from modelscope import snapshot_download
import os
import shutil
from pathlib import Path
import torch
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
from PIL import Image
import cv2
import numpy as np
import io
import base64
from mcp.server import FastMCP
import json


mcp = FastMCP("xunishizhuang_mcp")

model_dir = snapshot_download('cubeai/face-parsing')
print(model_dir)
# # 把模型文件夹复制到当前目录下
# if not os.path.exists(Path.cwd().absolute()/"face-parsing"):
#     shutil.copytree(model_dir, Path.cwd().absolute()/"face-parsing")

# 自动确定设备
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

# 加载模型
image_processor = SegformerImageProcessor.from_pretrained(model_dir,local_files_only=True)
model = SegformerForSemanticSegmentation.from_pretrained(model_dir,local_files_only=True)
# image_processor = SegformerImageProcessor.from_pretrained("cubeai/face-parsing")
# model = SegformerForSemanticSegmentation.from_pretrained("cubeai/face-parsing")
model.to(device)


def preprocess_image(image_path):
    """
    使用Segformer模型进行人脸解析，获取人脸各部位的分割掩码。

    参数：
        image_path (str): 输入图像的文件路径。

    返回：
        labels (numpy.ndarray): 人脸各部位的分割掩码，其中每个像素值代表对应的部位类别。
    """
    if not isinstance(image_path, Image.Image):
        image = Image.open(image_path)
    else:
        image = image_path
    inputs = image_processor(images=image, return_tensors="pt").to(device)
    outputs = model(**inputs)
    logits = outputs.logits
    upsampled_logits = torch.nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False
    )
    labels = upsampled_logits.argmax(dim=1)[0]
    return labels.cpu().numpy()


def sharpen(img):
    """
    对图像进行锐化处理。

    参数：
        img (numpy.ndarray): 输入图像。

    返回：
        img_out (numpy.ndarray): 锐化处理后的图像。
    """
    img = img * 1.0
    gauss_out = cv2.GaussianBlur(img, (5, 5), 0)

    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255
    return np.array(img_out, dtype=np.uint8)


def apply_makeup_class(source_img, source_parsing, reference_parsing, reference_img, part_id):
    """
    优化后的妆容迁移算法，根据参考图像的人脸解析结果，将参考图像中相应部位的颜色应用到源图像上。

    参数：
        source_img (numpy.ndarray): 源图像。
        source_parsing (numpy.ndarray): 源图像的人脸解析结果。
        reference_parsing (numpy.ndarray): 参考图像的人脸解析结果。
        reference_img (numpy.ndarray): 参考图像。
        part_id (int): 人脸部位的类别索引。

    返回：
        changed (numpy.ndarray): 应用妆容后的图像。
    """
    # 创建源图像和参考图像的部位掩码
    source_part_mask = np.zeros_like(source_parsing)
    source_part_mask[source_parsing == part_id] = 1

    reference_part_mask = np.zeros_like(reference_parsing)
    reference_part_mask[reference_parsing == part_id] = 1

    # 如果没有匹配的区域，直接返回原图
    if np.sum(source_part_mask) == 0 or np.sum(reference_part_mask) == 0:
        return source_img.copy()

    # 创建结果图像的副本
    result_img = source_img.copy()

    # 1. 为嘴唇(12或13)和眉毛等部位使用更复杂的色彩迁移
    if part_id in [0]:  # 嘴唇、眉毛、头发
        # 使用直方图匹配而不是简单的颜色替换
        # 转换到HSV颜色空间
        source_hsv = cv2.cvtColor(source_img, cv2.COLOR_BGR2HSV)
        ref_hsv = cv2.cvtColor(reference_img, cv2.COLOR_BGR2HSV)

        # 提取参考色和目标色
        ref_mean_hue = cv2.mean(ref_hsv, mask=reference_part_mask.astype(np.uint8))[0]
        ref_mean_sat = cv2.mean(ref_hsv, mask=reference_part_mask.astype(np.uint8))[1]

        # 获取源图像目标区域的平均值
        src_mean_hue = cv2.mean(source_hsv, mask=source_part_mask.astype(np.uint8))[0]
        src_mean_sat = cv2.mean(source_hsv, mask=source_part_mask.astype(np.uint8))[1]

        # 避免除零错误和极端值
        epsilon = 1e-6  # 一个很小的值，避免除零
        src_mean_hue = max(src_mean_hue, epsilon)
        src_mean_sat = max(src_mean_sat, epsilon)

        # 调整源图像的色调和饱和度
        source_hsv = source_hsv.astype(np.float32)  # 转换为浮点类型进行计算
        source_hsv[:, :, 0] = (source_hsv[:, :, 0] * (ref_mean_hue / src_mean_hue))
        source_hsv[:, :, 1] = (source_hsv[:, :, 1] * (ref_mean_sat / src_mean_sat))

        # 确保色调在 [0, 179] 范围内，饱和度和亮度在 [0, 255] 范围内
        source_hsv[:, :, 0] = np.clip(source_hsv[:, :, 0], 0, 179)
        source_hsv[:, :, 1:] = np.clip(source_hsv[:, :, 1:], 0, 255)

        # 转换回 8 位整数
        source_hsv = source_hsv.astype(np.uint8)

        # 转换回BGR并应用到结果图像
        changed = cv2.cvtColor(source_hsv, cv2.COLOR_HSV2BGR)

        # 仅更新目标区域
        result_img[source_part_mask == 1] = changed[source_part_mask == 1]

        # 对于头发增加锐化处理
        if part_id == 17:
            # 创建头发掩码
            hair_mask = np.zeros_like(source_parsing)
            hair_mask[source_parsing == 17] = 1

            # 对头发区域进行锐化
            hair_region = result_img[hair_mask == 1]
            sharpened_hair = cv2.detailEnhance(hair_region, sigma_s=10, sigma_r=0.15)
            result_img[hair_mask == 1] = sharpened_hair

    # 2. 对于其他面部区域采用更平滑的色彩迁移
    else:
        # 创建参考颜色的HSV表示
        ref_color = cv2.mean(reference_img, mask=reference_part_mask.astype(np.uint8))[:3]
        ref_color_bgr = np.array(ref_color, dtype=np.uint8).reshape(1, 1, 3)
        ref_color_hsv = cv2.cvtColor(ref_color_bgr, cv2.COLOR_BGR2HSV)

        # 转换源图像到HSV
        source_hsv = cv2.cvtColor(source_img, cv2.COLOR_BGR2HSV)

        # 仅调整目标区域的色调和饱和度
        source_hsv[source_part_mask == 1, 0] = ref_color_hsv[0, 0, 0]
        source_hsv[source_part_mask == 1, 1] = ref_color_hsv[0, 0, 1]

        # 转换回BGR并应用到结果图像
        changed = cv2.cvtColor(source_hsv, cv2.COLOR_HSV2BGR)
        result_img[source_part_mask == 1] = changed[source_part_mask == 1]

    # 3. 添加边缘平滑处理，使妆容过渡更自然
    # 创建一个软化的掩码，边缘有一定的过渡
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated_mask = cv2.dilate(source_part_mask.astype(np.uint8), kernel, iterations=2)
    blurred_mask = cv2.GaussianBlur(dilated_mask, (9, 9), 0)

    # 将模糊的掩码转换为三维，与图像形状匹配
    blurred_mask_3d = np.repeat(blurred_mask[:, :, np.newaxis], 3, axis=2)

    # 将原始图像和修改后的图像混合，基于模糊的掩码
    final_result = cv2.convertScaleAbs(
        source_img.astype(np.float32) * (1 - blurred_mask_3d) +
        result_img.astype(np.float32) * blurred_mask_3d
    )

    return final_result


def pil_to_cv2(pil_image):
    # 将 PIL.Image.Image 转换为 OpenCV 支持的 NumPy 数组格式
    # PIL.Image 使用的是 RGB 通道顺序，而 OpenCV 使用的是 BGR，所以需要转换
    cv2_image = np.array(pil_image)
    # 如果需要 BGR 格式（OpenCV 默认），则进行通道转换
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)
    return cv2_image

def cv2_to_pil(cv2_image):
    # cv2.imread 读取的图片是 BGR 格式，而 PIL.Image.Image 使用的是 RGB 格式
    # 需要先将 BGR 转换为 RGB
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    # 将 NumPy 数组转换为 PIL.Image.Image
    pil_image = Image.fromarray(rgb_image)
    return pil_image

def save_parse(parsing,save_path,is_save=True):
    """
    测试函数，用于可视化人脸解析结果。
    """
    parsing = cv2.normalize(parsing, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_32F)
    parsing = parsing.astype(np.uint8)
    colormap = cv2.applyColorMap(parsing, cv2.COLORMAP_VIRIDIS)
    if is_save:
        cv2.imwrite(save_path, colormap)
    colormap = cv2_to_pil(colormap)
    return colormap


def image_to_base64(image):
    """将PIL图像转换为base64"""
    if image is None:
        return None

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def base64_to_image(b64_string):
    """将base64转换为PIL图像"""
    if not b64_string:
        return None

    try:
        image_data = base64.b64decode(b64_string)
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception as e:
        print(f"base64转图像失败: {e}")
        return None

@mcp.tool()
def makeup_transfer(face_image, refer_image, parts=None):
    """
    实现妆容迁移，将参考图像的妆容迁移到源图像上。

    参数：
        source_image_path (str): 源图像的文件路径。
        reference_image_path (str): 参考图像的文件路径。
        output_image_path (str): 输出图像的文件路径。
        parts (list, 可选): 指定要进行妆容迁移的人脸部位类别索引。默认为 None，表示进行全脸妆容迁移。

    返回：
        result_img (numpy.ndarray): 妆容迁移后的图像。
    """
    # 获取源图像和参考图像的人脸解析结果
    # source_parsing = preprocess_image(source_image_path)
    # source_result = save_parse(source_parsing.copy(), 'assets/source_parsing.jpg')
    # reference_parsing = preprocess_image(reference_image_path)
    # reference_result = save_parse(reference_parsing.copy(), 'assets/reference_parsing.jpg')

    # 加载源图像和参考图像
    # if not isinstance(source_image_path, Image.Image):
    #     source_img = cv2.imread(source_image_path)
    # else:
    #     # 把Image对象转换为numpy数组
    #     source_img = pil_to_cv2(source_image_path)
    # if not isinstance(reference_image_path, Image.Image):
    #     reference_img = cv2.imread(reference_image_path)
    # else:
    #     # 把Image对象转换为numpy数组
    #     reference_img = pil_to_cv2(reference_image_path)

    source_image_path = face_image
    reference_image_path = refer_image
    source_image_path = base64_to_image(source_image_path)
    source_parsing = preprocess_image(source_image_path)
    reference_image_path = base64_to_image(reference_image_path)
    reference_parsing = preprocess_image(reference_image_path)
    source_result = save_parse(source_parsing.copy(), 'assets/source_parsing.jpg')

    source_img = pil_to_cv2(source_image_path)
    reference_img = pil_to_cv2(reference_image_path)

    # 如果未指定部位，则进行全脸妆容迁移
    if parts is None:
        # parts = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12 , 13, 15, 16, 17]  # 假设 1 到 18 是与妆容相关的类别
        parts = [1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 15]  # 假设 1 到 18 是与妆容相关的类别

    result_img = source_img.copy()

    # 对每个指定部位应用妆容
    for part_id in parts:
        result_img = apply_makeup_class(result_img, source_parsing, reference_parsing, reference_img, part_id)

    # 保存结果图像
    # cv2.imwrite(output_image_path, result_img)
    result_img = cv2_to_pil(result_img)
    result_img = image_to_base64(result_img)
    source_result = image_to_base64(source_result)
    return result_img, source_result
    # return 'image1','image2'

if __name__ == '__main__':
    mcp.run()
