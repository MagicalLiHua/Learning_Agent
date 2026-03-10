import dotenv
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_ollama import ChatOllama

# 加载环境变量配置文件
dotenv.load_dotenv()

# 创建同步Playwright浏览器实例
sync_browser = create_sync_playwright_browser()

# 从浏览器实例创建PlayWright工具包
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)

# 获取工具包中的所有工具
tools = toolkit.get_tools()

# 从Hub拉取OpenAI工具代理的提示模板
prompt = hub.pull("hwchase17/openai-tools-agent")

# 创建ChatOllama语言模型实例，使用qwen3:8b模型
llm = ChatOllama(base_url="http://10.160.108.2:11434",model="qwen3-vl:8b")

# 创建OpenAI工具代理，整合语言模型、工具和提示模板
agent = create_openai_tools_agent(llm, tools, prompt)

# 创建代理执行器，用于执行代理任务并管理工具调用
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    # 定义任务
    command = {
        "input": "访问这个网站https://www.cuiliangblog.cn/detail/section/227788709 并帮我总结一下这个网站的内容"
    }

    # 执行任务
    response = agent_executor.invoke(command)
    print(response)