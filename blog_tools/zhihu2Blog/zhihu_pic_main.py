
import os
import re
from zhihu_pic_utils import *
def process_markdown_and_images(md_path):
    # 0. 创建processing文件夹，并将md的副本放入其中
    processing_path = os.path.join(md_path, "processing")
    md_file_path = copy_md_files(md_path, processing_path)
    # 1. 下载md中的图片，并放入image文件夹下
    image_folder = os.path.join(processing_path, "pic/image_WaterMark")
    os.makedirs(image_folder, exist_ok=True)
    with open(md_file_path, "r", encoding="utf-8") as file:
        md_content = file.read()
    image_urls = re.findall(r'!\[.*?\]\((https?://.*?\.(?:jpg|png|webp|jpeg)(?:\?.*?)?)\)', md_content)
    WaterMark_img_downloader(image_urls, image_folder)
    #处理webp图片为jpg
    webp2jpg(image_folder,image_folder)
    #删除webp图片
    delete_webp(image_folder)
    # 2. 替换图片链接和知乎相关内容
    folder_name = next(filename.replace(".md", "") for filename in os.listdir(md_path) if filename.endswith(".md"))
    for url in image_urls:
        file_name = os.path.basename(url.split('?source=')[0])
        if file_name.endswith(".webp"):
            file_name = file_name.replace(".webp", ".jpg")
        new_path = f"/images/{folder_name}/{file_name}"
        md_content = md_content.replace(url, new_path)
    md_content = md_content.replace('//link.zhihu.com/?target=https%3A', '')
    pattern = r'(https://zhida\.zhihu\.com/search\?.*?=entity)'
    md_content = re.sub(pattern, "", md_content)
    with open(md_file_path, "w", encoding="utf-8") as file:
        file.write(md_content)
    print("md文档内容修改完成！")
    # 3. 读取【element.txt】，下载无水印版图片
    ele_file_path = os.path.join(md_path, "element.txt")
    img_no_watermark = os.path.join(processing_path, "pic/a_no_watermark")
    zhihu_NoWaterMark_pic_downloader(ele_file_path, img_no_watermark)
    # 4. 将无水印图片匹配并重命名，放入与父文件夹相同命名的子文件夹中
    target_folder = os.path.join(processing_path, folder_name)
    match_and_rename_images(image_folder, img_no_watermark, target_folder)
    print(f"博客图文处理完成！处理结果请查看目录：{processing_path}")
if __name__ == "__main__":
    #该路径不要有中文
    md_path = r'C:\Users\konglingda\Desktop\mine_data\BLOGS'
    process_markdown_and_images(md_path)
