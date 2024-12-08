
import os
import shutil
import re
import requests
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from pathlib import Path
def copy_md_files(source_path, dest_path):
    """
    查找源路径下的所有 .md 文件，并将其复制到目标路径。
    Args:
        source_path: 源路径字符串。
        dest_path: 目标路径字符串。
    """
    if not os.path.exists(source_path):
        print(f"错误：源路径 '{source_path}' 不存在。")
        return
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
        # print(f"已创建目标路径 '{dest_path}'。")
    for filename in os.listdir(source_path):
        if filename.endswith(".md"):
            source_file = os.path.join(source_path, filename)
            dest_file = os.path.join(dest_path, filename)
            try:
                shutil.copy2(source_file, dest_file) # 使用copy2保留元数据
                # print(f"已复制 '{filename}' 到 '{dest_path}'。")
            except Exception as e:
                print(f"复制 '{filename}' 失败：{e}")
    return dest_file
def WaterMark_img_downloader(image_urls,image_folder):
    # 处理webp格式的
    image_urls =[i.split('?source=')[0] for i in image_urls] 
        # 下载图片并保存
    for url in image_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            # 获取图片名
            image_name = os.path.basename(url)
            image_path = os.path.join(image_folder, image_name)
            # 保存图片
            with open(image_path, "wb") as img_file:
                img_file.write(response.content)
            print(f"已下载图片: {url}")
        except requests.exceptions.RequestException as e:
            print(f"下载图片失败: {url} 错误信息: {e}")
    print("md文档内图片下载完成。")

def zhihu_NoWaterMark_pic_downloader(file_path,image_folder):
    # 创建保存图片的文件夹
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    # 读取txt文档内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 将图片网址换行处理
    content = content.replace('</p><figure data-size="normal">', '\n')
    # 正则表达式匹配原始数据
    patterns = [
        r'(?=.*data-original="([^"]+)")(?=.*data-actualsrc="([^"]+)")(?=.*data-original-token="([^"]+)").*',
        r'(?=.*data-original="([^"]+)")(?=.*src="([^"]+)")(?=.*data-original-token="([^"]+)").*'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content)
        if matches:
            break


    # print('匹配项：', matches)
    # 构造三列数据
    data_actualsrc = []
    data_original_token = []
    data_replaced = []
    src_data = []
    for original, actualsrc, token in matches:
        if actualsrc =='':
            actualsrc=original
        data_actualsrc.append(actualsrc)
        data_original_token.append(token)
        replaced = actualsrc.replace(actualsrc.split('/')[-1], token) + '.jpg'
        data_replaced.append(replaced)
        # 构建 src 列数据
        webp_filename = original.split('/')[-1].replace('_r.jpg', '.webp')
        src = f'<img src="https://pic1.zhimg.com/{webp_filename}" />'
        src_data.append(src)
    # 打印结果并下载图片
    for i in range(len(data_actualsrc)):
        url = data_replaced[i]  # data-replaced
        try:
            response = requests.get(url)
            response.raise_for_status()
            # 获取图片名
            image_name = os.path.basename(url)
            image_path = os.path.join(image_folder, image_name)
            # 保存图片
            with open(image_path, "wb") as img_file:
                img_file.write(response.content)
            print(f"已下载图片: {url}")
        except requests.exceptions.RequestException as e:
            print(f"下载图片失败: {url} 错误信息: {e}")
    print('--------无水印图下载结束--------')
def copy_folder_contents(rename_folder, target_folder):
    """
    将 rename_folder 中的所有文件和文件夹复制到 target_folder 中.
    Args:
        rename_folder: 源文件夹路径.
        target_folder: 目标文件夹路径.
    """
    try:
        # 检查源文件夹是否存在
        if not os.path.exists(rename_folder):
            raise FileNotFoundError(f"源文件夹 '{rename_folder}' 不存在.")
        # 确保目标文件夹存在
        os.makedirs(target_folder, exist_ok=True)
        for item in os.listdir(rename_folder):
            source_item = os.path.join(rename_folder, item)
            target_item = os.path.join(target_folder, item)
            # 如果是文件，直接复制
            if os.path.isfile(source_item):
                shutil.copy2(source_item, target_item)  # copy2 保留元数据
            # # 如果是文件夹，递归复制
            # elif os.path.isdir(source_item):
            #     shutil.copytree(source_item, target_item, dirs_exist_ok=True) # dirs_exist_ok 避免目标文件夹已存在时的错误

    except FileNotFoundError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"复制过程中发生错误: {e}")
    else:
        print(f"已成功将 '{rename_folder}' 中的内容复制到 '{target_folder}'.")

#图片匹配重命名
def load_image(file_path):
    return cv2.imread(file_path)
def get_image_similarity(img1, img2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Resize images to have the same dimensions
    height = min(gray1.shape[0], gray2.shape[0])
    width = min(gray1.shape[1], gray2.shape[1])
    gray1 = cv2.resize(gray1, (width, height))
    gray2 = cv2.resize(gray2, (width, height))
    
    # Compute SSIM between the two images
    similarity = ssim(gray1, gray2)
    return similarity
def match_and_rename_images(orn_folder, rename_folder,target_folder):
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    orn_images = [f for f in os.listdir(orn_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    rename_images = [f for f in os.listdir(rename_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    for rename_img in rename_images:
        rename_path = os.path.join(rename_folder, rename_img)
        img_to_rename = load_image(rename_path)
        
        best_match = None
        highest_similarity = -1
        for orn_img in orn_images:
            orn_path = os.path.join(orn_folder, orn_img)
            orn_image = load_image(orn_path)
            
            similarity = get_image_similarity(img_to_rename, orn_image)
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = orn_img
        if best_match:
            new_name = os.path.join(rename_folder, best_match)
            os.rename(rename_path, new_name)
            print(f"Renamed {rename_img} to {best_match}")
        else:
            print(f"No match found for {rename_img}")
    copy_folder_contents(orn_folder,target_folder)
    copy_folder_contents(rename_folder,target_folder)



# 转换并保存为WebP格式
def convert_jpg_to_webp(directory):
    # 确保目录路径存在
    directory = Path(directory)
    if not directory.exists():
        print(f"目录 {directory} 不存在!")
        return
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            # 构建完整的文件路径
            filepath = directory / filename
            
            # 打开图像
            with Image.open(filepath) as img:
                # 构建新的WebP文件名
                webp_filename = filepath.with_suffix(".webp")
                
                # 转换并保存为WebP格式
                img.save(webp_filename, "WEBP")
            
            print(f"已转换: {filename} -> {webp_filename.name}")
    # print("转换完成!")
def webp2jpg(input_folder,output_folder):
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 遍历输入文件夹中的所有 .webp 文件并转换为 .jpg 格式
    for filename in os.listdir(input_folder):
        if filename.endswith('.webp'):
            webp_path = os.path.join(input_folder, filename)
            jpg_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpg')
            
            # 打开 .webp 文件并保存为 .jpg 格式
            with Image.open(webp_path) as img:
                img.convert('RGB').save(jpg_path, 'JPEG')
            
            print(f'Converted {webp_path} to {jpg_path}')
    # print('Conversion complete!')

def delete_webp(directory):
    # 确保目录路径存在
    directory = Path(directory)
    if not directory.exists():
        print(f"目录 {directory} 不存在!")
        return
    
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(".webp"):
            # 构建完整的文件路径
            filepath = directory / filename                
            # 删除文件
            os.remove(filepath)
            print(f"已删除: {filename}")
