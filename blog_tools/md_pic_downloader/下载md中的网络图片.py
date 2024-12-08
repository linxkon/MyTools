import os
import re
import requests

# 创建保存图片的文件夹
image_folder = "image"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# 读取Markdown文件内容
md_file_path = r"C:\Users\10921\Desktop\一. RTE常见问题.md"
with open(md_file_path, "r", encoding="utf-8") as file:
    md_content = file.read()

# 匹配Markdown文件中的图片链接
image_urls = re.findall(r'!\[.*?\]\((http.*?\.(?:jpg|png))\)', md_content)

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

print("所有图片下载完成。")
