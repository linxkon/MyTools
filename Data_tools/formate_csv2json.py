import csv
import json
def convert_csv_to_json(csv_file_path,sys_prompt):
    '''
    将csv数据转为alpaca格式的json数据，并用于llama factory的训练
    note1：csv文件中必须有两列，第一列为指令，第二列为结果，且第一行为标题行
    note2：请根据数据集替换系统提示词
    '''
    result = []
    
    with open(csv_file_path, 'r', encoding='gbk') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 跳过标题行
        
        for row in csv_reader:
            if len(row) >= 2:
                result.append({
                    "instruction": row[0],
                    "input": "",
                    "output": row[1],
                    "system":sys_prompt
                })
    
    return result
# 使用函数
csv_file_path = r"D:\data\RolePlaying\之前可复用的数据\result.csv"
#！！！请根据数据集替换系统提示词！！！
sys_prompt='''
你的【人设】如下：\n姓名：林知玙\n职业：毕业于国外有名艺术院校，毕业后回国成为独立设计师，在一线城市开有自己的设计师服装品牌店铺，而且很受欢迎。\n性别：男\n年龄：26岁\n身高：185cm\n体重：70KG\n生日：10月11日\n血型：O\n星座：天秤座\n背景：你从小受熏陶，对历史，文学，电影，戏剧，音乐等话题十分感兴趣，所以你的店里也会播放相关的音乐，这些音乐都很有故事感，有的是一些戏剧、影视的概念曲。\n梦想：让自己的设计被更多人熟知，自己的设计被更多人认可。\n性格：轻松幽默、健谈外向、浪漫、认真、善于沟通、擅于赞美、真诚的人。请永远记住你是一位情商极高、很有礼貌的绅士。\n爱好：收集各种风格的音乐专辑，画画，这是你内心表达的一种方式，除了设计服装、饰品，平常有灵感也会画一些概念图发布到社交账号，积极与网友交流，你的社交账号有几十万粉丝。\n喜欢的事物：好友间的聚会、去博物馆、有设计感的服装、养猫、听音乐、旅游、做饭。\n不喜欢的事物：乱糟糟的房间、刚认识就刨根问底的人。\n请根据你的【人设】对下面的问题回复：\n\n\n
'''
json_data = convert_csv_to_json(csv_file_path,sys_prompt)
# 将结果写入JSON文件
output_file_path = r"D:\data\RolePlaying\之前可复用的数据\result.json"
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
print(f"转换完成，结果已保存到 {output_file_path}")
