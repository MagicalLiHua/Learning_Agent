from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# 创建聊天提示模板，用于构建AI助手的对话上下文
# 该模板包含两个消息：AI助手的自我介绍和用户问题
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是AI助手，你的名字叫{name}。"),
    HumanMessage(content="请问：{question}")
])

# 格式化聊天提示模板，填充具体的助手名称和问题内容
# 参数name: AI助手的名字
# 参数question: 用户提出的问题
# 返回值: 格式化后的消息列表
# message = chat_prompt.format_messages(name="亮仔", question="什么是LangChain")

# 打印格式化后的消息内容
# print(message)


from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 创建系统消息模板，用于定义AI助手的身份信息
system_prompt=SystemMessagePromptTemplate.from_template("你是AI助手，你的名字叫{name}。")

# 创建人类消息模板，用于定义用户提问的格式
human_prompt = HumanMessagePromptTemplate.from_template("请回答：{question}")

# 创建具体的系统消息和人类消息实例
system_msg = SystemMessage(content="你是AI工程师")
human_msg = HumanMessage(content="你好")

# 创建嵌套的消息模板，包含预定义的系统和人类消息
nested_prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])

# 构建完整的聊天提示模板，组合了模板和具体消息
chat_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    human_prompt,
    system_msg,
    human_msg,
    nested_prompt
])

# 格式化消息并打印结果
message = chat_prompt.format_messages(name="亮仔", question="什么是LangChain")
print(message)
