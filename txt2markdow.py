import re

def process_line(line):
    """处理少于40个字符的行，识别并转换标题等级。"""
    line = line.strip()
    # breakpoint()
    if 1< len(line) < 40 and (line[0].isdigit() or line.startswith('#') or line.startswith('*')):
        line = line.replace('#', '').replace('*', '').strip()
        if line[0].isdigit():
        # breakpoint()
        # 识别标题等级
            match = re.match(r"^(\d{1,2}\.)?(\d{1,2}\.)?(\d{1,2}\.)?(\d{1,2}\.)?", line)
            if match:
                level = match.groups().count(None) # 计算None的数量来判断等级
                if level == 0:
                    return "##### " +  '*'+line +  '*'+"\n"  # 5级标题
                elif level == 1:
                    return "#### " + '*'+line +  '*'+"\n"  # 4级标题
                elif level == 2:
                    return "### " + '**'+line + '**'+"\n"  # 3级标题
                elif level == 3:
                    return "## " + '**'+line + '**'+"\n"  # 2级标题
                elif level == 4 :
                    return "# " + '**'+line + '**'+"\n"  # 1级标题
                
        else:
            return line + "\n"
    return line + "\n"



def process_line_main():
    """读取文件，处理每一行，并保存为Markdown文件。"""
    input_file = "C:\\Users\\10921\\Desktop\\artical.txt"
    output_file = "artical.md"

    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            processed_line = process_line(line)
            if processed_line:
                f_out.write(processed_line)
    
    print('work done!')

if __name__ == "__main__":
    process_line_main()
    # l1='#### **2. 偏见与包容性**'
    # l2='#### ***2.2 幻觉现象***'
    # l3='**•新兴趋势和未来方向：**分类讨论各个领域的最新发展并展望未来方向。'
    # print(process_line(l1))
    # print(process_line(l2))
    # print(process_line(l3))
