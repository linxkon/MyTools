import re
def clean_text(text):
    '''
    将英文转化为小写
    去除HTML标签、
    去除URL链接、
    去除邮箱地址、
    去除其他特殊字符**等非文本信息：
    '''
    text = text.lower() # 将英文字符转换为小写
    text = re.sub(r'<[^>]+>', '', text)  # 移除HTML标签
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)  # 移除URL
    text = re.sub(r'\S*@\S*\s?', '', text)  # 移除邮箱地址
    text = re.sub(r'[^\w\u4e00-\u9fff\s]', '', text) # 去除特殊字符
    return text