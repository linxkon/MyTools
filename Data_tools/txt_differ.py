import os
import difflib

# 指定文件夹路径
folder_path = r'C:\Users\10921\Desktop\tools\AI_tools'

# 获取文件夹中的所有txt文件
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

if len(txt_files) < 2:
    print("文件夹中没有足够的txt文件进行比较")
else:
    # 读取两个文件的内容
    with open(os.path.join(folder_path, txt_files[0]), 'r', encoding='utf-8') as f1:
        content1 = f1.readlines()
    with open(os.path.join(folder_path, txt_files[1]), 'r', encoding='utf-8') as f2:
        content2 = f2.readlines()

    # 比较文件内容
    matcher = difflib.SequenceMatcher(None, content1, content2)
    same_content = []
    different_content = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            same_content.extend(content1[i1:i2])
        elif tag in ('replace', 'delete', 'insert'):
            different_content.extend(content1[i1:i2])
            different_content.extend(content2[j1:j2])

    # 创建相同内容的文件
    with open(os.path.join(folder_path, 'same_content.txt'), 'w', encoding='utf-8') as f:
        f.writelines(same_content)

    # # 创建不同内容的文件
    # with open(os.path.join(folder_path, 'different_content.txt'), 'w', encoding='utf-8') as f:
    #     f.writelines(different_content)

    print("比较完成。请查看'same_content.txt'和'different_content.txt'文件。")
