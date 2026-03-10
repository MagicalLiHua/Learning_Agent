from datetime import datetime
import dotenv
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

# 加载环境变量配置文件
dotenv.load_dotenv()


@tool
def summarize_website(url: str) -> str:
    """
    访问指定网站并返回内容总结。

    参数:
        url (str): 要访问和总结的网页URL。

    返回:
        str: 网页正文内容的总结，若失败则返回错误信息。
    """
    try:
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
        command = {
            "input": f"访问这个网站 {url} 并帮我详细总结这个网页的正文内容，评论交流区、版权信息、友情链接等其他内容不要总结。"
        }
        result = agent_executor.invoke(command)
        return result.get("output", "无法获取网站内容总结")

    except Exception as e:
        return f"网站访问失败: {str(e)}"


@tool
def save_file(summary: str) -> str:
    """
    将文本内容生成为md文件。

    参数:
        summary (str): 需要保存为文件的内容。

    返回:
        str: 保存成功的文件名路径信息。
    """
    filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# 网页内容总结\n\n")
        f.write(summary)
    return f"已保存至 {filename}"


# 初始化格式化语言模型
format_llm = ChatOllama(base_url="http://10.160.108.2:11434",model="qwen3-vl:8b")

# 定义格式化提示模板，用于优化总结内容以适应MD文件格式
format_prompt = ChatPromptTemplate.from_template(
    """请优化以下网站总结内容，使其更适合MD文件格式：

    原始总结：
    {summary}

    优化后的内容："""
)

# 创建字符串输出解析器
format_parser = StrOutputParser()

# 构建格式化处理链：模板 -> 模型 -> 解析器
format_chain = format_prompt | format_llm | format_parser

# 构建主流程链：网站总结 -> 格式化 -> 保存文件
chain = (
        summarize_website
        | (lambda summary: {"summary": summary})
        | format_chain
        | save_file
)

# 执行整个流程链，传入目标URL进行网站内容总结与保存
chain.invoke({"url": "https://python.langchain.ac.cn/docs/introduction/"})