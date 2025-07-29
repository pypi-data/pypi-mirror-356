from openai import OpenAI

def run():
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="e5a2fafe-a448-483f-964c-1a08e470dfb1",
    )
    # 提示用户输入问题（支持多行）
    print("input:")
    user_input = []
    try:
        while True:
            # 逐行读取输入
            line = input()
            # 检测到"退出"立即结束输入
            if line.strip().lower() == "退出":
                break
            user_input.append(line)
    except EOFError:
        pass  # 正常结束输入

    # 如果没有输入内容直接退出
    if not user_input:
        print("未输入内容，程序退出")
        return

    user_content = "\n".join(user_input)

    # 调用API
    resp = client.chat.completions.create(
        model="doubao-pro-256k-241115",
        messages=[{"content": user_content, "role": "user"}],
        stream=True,
    )

    # 流式输出响应
    for chunk in resp:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

run()