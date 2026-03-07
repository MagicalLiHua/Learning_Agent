import asyncio
import httpx


# ------------------------------------------------
# 核心基类：所有 LangChain 组件的祖先
# ------------------------------------------------
class Runnable:
    # 这个魔法方法，让我们可以使用 prompt | model 这样的语法
    def __or__(self, other):
        # 当执行 a | b 时，实际上是创建了一个包含 a 和 b 的流水线
        return RunnableSequence(self, other)

    async def ainvoke(self, input_data):
        raise NotImplementedError("子类必须实现这个方法")


# ------------------------------------------------
# 流水线类：负责把两个组件串起来跑
# ------------------------------------------------
class RunnableSequence(Runnable):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    async def ainvoke(self, input_data):
        # ------------------------------------------------
        # 👇 思考题填空：
        # 这里是 LCEL 链条运行的核心！
        # 我们有 self.first (上游组件) 和 self.second (下游组件)。
        # 它们都有 `ainvoke` 这个异步方法。
        # 你该如何编写代码，让数据从上游流向下游，并返回最终结果？
        # ------------------------------------------------
        step1_result = await self.first.ainvoke(input_data)  # 上游组件处理输入数据
        final_result = await self.second.ainvoke(step1_result)  # 下游组件处理上游的结果
        return final_result


# ------------------------------------------------
# 组件 1：提示词模板 (PromptTemplate)
# ------------------------------------------------
class PromptTemplate(Runnable):
    def __init__(self, template_str):
        self.template_str = template_str

    async def ainvoke(self, input_dict):
        # 把字典里的变量替换到字符串中
        formatted_prompt = self.template_str.format(**input_dict)
        print(f"📝 提示词组装完毕: {formatted_prompt}")
        return formatted_prompt


# ------------------------------------------------
# 组件 2：大型语言模型 (LLM)
# ------------------------------------------------
class QwenLLM(Runnable):
    def __init__(self, url, model_name):
        self.url = url
        self.model_name = model_name

    async def ainvoke(self, prompt_text):
        print(f"🧠 模型正在思考...")

        # 注意：ChatPromptTemplate 现在返回的是一个消息列表 (list of dict)
        # 而不是简单的字符串，所以这里 payload 的 messages 逻辑需要微调
        payload = {
            "model": self.model_name,
            "messages": prompt_text,  # 这里的 prompt_text 其实是 ChatPromptTemplate 传过来的 messages 列表
            "stream": False  # 确保关闭流式输出，方便直接解析 json
        }

        async with httpx.AsyncClient(trust_env=False) as client:
            try:
                response = await client.post(self.url, json=payload, timeout=30.0)
                # 打印出结果，方便调试。如果报错了，你能直接看到原因
                result = response.json()

                if "choices" not in result:
                    print(f"❌ 接口返回异常: {result}")
                    return f"错误：模型返回了非预期格式。原信息：{result}"

                return result["choices"][0]["message"]["content"]
            except Exception as e:
                return f"连接模型失败: {str(e)}"


# ------------------------------------------------
# 组件 3：输出解析器 (OutputParser)
# ------------------------------------------------
class KeywordsParser(Runnable):
    async def ainvoke(self, text):
        print(f"🔍 解析器正在处理输出...")
        # 模拟一个简单的逻辑：去掉标点，取前三个词作为关键词
        # 实际开发中，这里可能会用正则或者另一个 LLM 来处理
        clean_text = text.replace("！", "").replace("。", "").replace("，", "")
        keywords = clean_text.split()[:3]
        return {
            "original_reply": text,
            "keywords": keywords
        }


class ChatPromptTemplate(Runnable):
    def __init__(self, system_msg):
        # 初始化时，我们给大模型一个人设
        self.system_msg = system_msg

    async def ainvoke(self, input_dict):
        # 1. 把传入的变量提取出来
        history = input_dict.get("history", [])  # 默认是空列表
        new_question = input_dict.get("topic")

        # 2. 先把系统设定装进列表
        messages = [
            {"role": "system", "content": self.system_msg}
        ]

        # ------------------------------------------------
        # 👇 填空：拼装记忆和新问题
        # 现在我们手里有：
        # 1. messages (目前只有一个 system 字典)
        # 2. history (一个包含之前对话字典的列表)
        # 3. new_question (用户的新问题，字符串)
        #
        # 请编写代码，把 history 里的记录追加到 messages 里，
        # 并且把 new_question 也包装成 {"role": "user", "content": ...} 加到最后。
        # ------------------------------------------------

        # 1. 把 history 里的记录追加到 messages 里
        messages.extend(history)
        # 2. 把 new_question 也包装成 {"role": "user", "content": ...} 加到最后
        messages.append({"role": "user", "content": new_question})


        print(f"📝 包含记忆的提示词打包完毕！共 {len(messages)} 条消息。")
        return messages


# ================================================
# 🎬 导演开机：测试我们自己手搓的 LCEL
# ================================================
async def main():
    SERVER_URL = "http://10.160.108.2:11434/v1/chat/completions"
    MODEL = "qwen3-vl:8b"  # 换成你实际跑通的模型名

    # 1. 实例化组件
    prompt = ChatPromptTemplate("你是一个幽默的 AI 助手，说话喜欢带梗。")
    model = QwenLLM(SERVER_URL, MODEL)
    chain = prompt | model

    print("--- 🚀 聊天开始 (输入 '退出' 结束) ---")

    # 💾 这是我们抽离出来的“记忆存储区”
    chat_history = []

    while True:
        user_input = input("\n👤 你：")
        if user_input == "退出":
            break

        # 将用户的输入和当前的记忆一起传给流水线
        reply = await chain.ainvoke({
            "topic": user_input,
            "history": chat_history
        })

        print(f"🤖 AI：{reply}")

        # ------------------------------------------------
        # 👇 思考题填空：更新记忆存储区
        # 这一轮对话已经结束，但为了让下一轮对话 AI 能记住刚才发生的事，
        # 我们必须把刚刚的 user_input 和 reply 添加到 chat_history 中。
        # ------------------------------------------------

        # 请在这里写下更新 chat_history 的代码
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    asyncio.run(main())