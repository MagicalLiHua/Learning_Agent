import os
import dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# 加载环境变量配置文件
dotenv.load_dotenv()
# 从环境变量中获取Serper API密钥
api_key = os.getenv("SERPER_API_KEY")
# 创建Google Serper API包装器实例
api_wrapper = GoogleSerperAPIWrapper()

# 创建Google搜索工具实例
search_tool = GoogleSerperRun(api_wrapper=api_wrapper)
# 将搜索工具添加到工具列表中
tools = [search_tool]

# 定义聊天提示模板，包含系统角色设定、用户输入和代理执行过程占位符
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名助人为乐的助手，并且可以调用工具进行网络搜索，获取实时信息。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 创建Ollama聊天模型实例，使用qwen3:8b模型
llm = ChatOllama(base_url="http://10.160.108.2:11434",model="qwen3-vl:8b")

# 创建工具调用代理，整合语言模型、工具和提示模板
agent = create_tool_calling_agent(llm, tools, prompt)

# 创建代理执行器，用于执行代理并管理工具调用过程
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 调用代理执行器，传入用户查询问题
agent_executor.invoke({"input": "小米最近发布的新品是什么？"})