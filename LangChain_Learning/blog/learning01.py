from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

# 设置本地模型，不使用深度思考
model = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b")

# # 构建消息列表
# messages = [SystemMessage(content="你叫小亮，是一个乐于助人的人工助手"),
#             HumanMessage(content="你是谁")
#             ]
# # 调用大模型
# response = model.invoke(messages)
# # 打印结果
# print(response.content)
# print(type(response))


# 构建消息列表 流式输出
messages = [SystemMessage(content="你叫小亮，是一个乐于助人的人工助手"),
            HumanMessage(content="你是谁")
            ]
# 流式调用大模型
response = model.stream(messages)
# 流式打印结果
for chunk in response:
    print(chunk.content, end="",flush=True) # 刷新缓冲区 (无换行符，缓冲区未刷新，内容可能不会立即显示)
print("\n")
print(type(response))