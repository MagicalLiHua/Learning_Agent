import os
import dotenv
from langchain_ollama import ChatOllama
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langchain_community.tools import GoogleSerperRun
# 加载环境变量配置文件
dotenv.load_dotenv()
# 从环境变量中获取Serper API密钥
api_key = os.getenv("SERPER_API_KEY")
# 创建Google Serper API包装器实例
api_wrapper = GoogleSerperAPIWrapper()
# 创建Google搜索工具实例
search_tool = GoogleSerperRun(api_wrapper=api_wrapper)
# 初始化本地大语言模型，配置基础URL、模型名称和推理模式
llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)

# 定义工具列表，包含天气查询和结果写入工具
tools = [search_tool]

# 创建ReAct代理，结合语言模型和工具函数
agent = create_agent(model=llm, tools=tools)

# 调用工具处理用户查询
response = agent.invoke({"messages": [{"role": "user", "content": "小米最近发布的新品是什么？"}]})
# 输出完整响应结果和最终回答内容
print(response)
response["messages"][-1].pretty_print()