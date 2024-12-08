#说明:色彩反转.用于处理博客图片
import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def invert_rgba(image_path):
    # 打开图片
    image = Image.open(image_path)
    
    # 如果图片不是RGBA模式，先转换为RGBA
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # 获取图片数据
    data = image.getdata()
    
    # 创建新的像素数据
    new_data = [(255-item[0], 255-item[1], 255-item[2], item[3]) for item in data]
    
    # 创建新图片并设置数据
    inverted_image = Image.new('RGBA', image.size)
    inverted_image.putdata(new_data)
    
    return inverted_image

def process_images():
    # 创建tkinter根窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 打开文件选择对话框
    file_paths = filedialog.askopenfilenames(
        title="选择要转换的图片",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    if not file_paths:
        print("没有选择任何文件。")
        return

    # 处理每个选中的文件
    for file_path in file_paths:
        try:
            # 获取文件名和目录
            directory, filename = os.path.split(file_path)
            name, ext = os.path.splitext(filename)

            # 转换图片
            inverted = invert_rgba(file_path)

            # 创建新的文件名
            new_filename = f"{name}_inverted{ext}"
            new_path = os.path.join(directory, new_filename)

            # 保存反色图片
            inverted.save(new_path)
            print(f"已保存反色图片: {new_path}")

        except Exception as e:
            print(f"处理 {file_path} 时出错: {str(e)}")

    print("所有图片处理完成。")

# 运行程序
if __name__ == "__main__":
    process_images()
