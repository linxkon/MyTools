import os
from PIL import Image

# 设置输入和输出文件夹
input_folder = r'C:\Users\10921\Desktop\tools\pic\webp'
output_folder = r'C:\Users\10921\Desktop\tools\pic\output'

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

print('Conversion complete!')
