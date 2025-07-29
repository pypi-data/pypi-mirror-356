def pip():
    print("pip install 'volcengine-python-sdk[ark]'")
def run():
    from volcenginesdkarkruntime import Ark


    client = Ark(api_key="8da1eb82-6942-48ca-be1a-e037f2fece63")

    print("退出'：")
    messages = []
    user_content = ""

    # 收集多行用户输入
    while True:
        line = input()
        if line.strip() == "退出":  # 检测到单独的"退出"行
            break
        user_content += line + "\n"  # 保留换行符

    # 移除最后一个多余的换行符
    if user_content.endswith("\n"):
        user_content = user_content[:-1]

    # 添加用户消息到对话历史
    if user_content:
        messages.append({"role": "user", "content": user_content})
        print("\n111...\n")

        # 调用API获取回复
        completion = client.chat.completions.create(
            model="doubao-1-5-vision-pro-32k-250115",
            messages=messages
        )

        # 获取并打印AI回复
        ai_reply = completion.choices[0].message.content
        print(ai_reply)

        # 将AI回复添加到对话历史（可选，用于连续对话）

    else:
        print("未检测到有效输入内容")