import os
import re
import requests
#请输入html 的 body中 的元素值
def zhihu_pic(file_path):
    # 创建保存图片的文件夹
    image_folder = "image"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # 读取txt文档内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配原始数据
    pattern = re.compile(r'data-original="(https://[^"]+)" data-actualsrc="(https://[^"]+)" data-original-token="([^"]+)"')

    # 查找所有匹配项
    matches = pattern.findall(content)

    # 构造三列数据
    data_actualsrc = []
    data_original_token = []
    data_replaced = []
    src_data = []

    for original, actualsrc, token in matches:
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
        # print(f'data-actualsrc: {data_actualsrc[i]}')
        # print(f'data-original-token: {data_original_token[i]}')
        # print(f'data-replaced: {data_replaced[i]}')
        # print(f'src: {src_data[i]}')
        # print('-----------------------------------')

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

file_path=r"C:\Users\10921\Desktop\tools\知乎无水印.txt"
zhihu_pic(file_path=file_path)


