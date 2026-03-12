from langchain_ollama import ChatOllama
from tools import get_weather, write_file
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

# 初始化本地大语言模型，配置基础URL、模型名称和推理模式
llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)

# 定义工具列表，包含天气查询、写入文件工具
tools = [get_weather, write_file]

# 创建ReAct代理，结合语言模型和工具函数
agent = create_agent(model=llm, tools=tools)