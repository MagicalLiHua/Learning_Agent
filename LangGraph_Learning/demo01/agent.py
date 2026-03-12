from langchain_ollama import ChatOllama
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from tools import get_weather

# 初始化本地大语言模型，配置基础URL、模型名称和推理模式
llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)

# 定义工具列表，包含天气查询工具
tools = [get_weather]

# 创建ReAct代理，结合语言模型和工具函数
agent = create_agent(model=llm, tools=tools)

# 调用代理处理用户查询，获取北京天气信息
response = agent.invoke({"messages": [{"role": "user", "content": "请问北京今天天气如何？"}]})
# 输出完整响应结果和最终回答内容
print(response)
print(response["messages"][-1].content)
response["messages"][-1].pretty_print()
# 使用stream方法进行流式调用
for chunk in agent.stream(
        {"messages": [{"role": "user", "content": "请问北京今天天气如何？"}]},
        stream_mode="values",
):
    chunk["messages"][-1].pretty_print()

# 这里stream_mode有四种选项：
# - messages：流式输出大语言模型回复的token
# - updates : 流式输出每个工具调用的每个步骤。
# - values : 一次输出到所有的chunk。默认值。
# - custom : 自定义输出。主要是可以在工具内部使用get_stream_writer获取输入流，添加自定义的内容。