from zhipuai import ZhipuAI

# 请填写您自己的APIKey
client = ZhipuAI(api_key="xxx")

# 初始化对话历史
dialogue_history = []


def get_response(user_input):
    # 将用户输入添加到对话历史
    dialogue_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=dialogue_history,
        stream=True,
    )

    # 逐块处理响应，并打印每块中的内容
    generated_text = ""
    for chunk in response:
        generated_text += chunk.choices[0].delta.content

    # 将生成的回复添加到对话历史
    dialogue_history.append({"role": "assistant", "content": generated_text})

    return generated_text


# 循环进行对话
while True:
    user_input = input("你: ")
    if user_input.lower() in ["退出", "结束"]:
        print("对话结束。")
        break
    response = get_response(user_input)
    print("助手:", response)
