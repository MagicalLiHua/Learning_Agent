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
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt_text}],
            "temperature": 0.7
        }
        async with httpx.AsyncClient(trust_env=False) as client:
            response = await client.post(self.url, json=payload, timeout=30.0)
            result = response.json()
            return result["choices"][0]["message"]["content"]


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


# ================================================
# 🎬 导演开机：测试我们自己手搓的 LCEL
# ================================================
async def main():
    SERVER_URL = "http://10.160.108.2:11434/v1/chat/completions"
    MODEL = "qwen3-vl:8b"  # 换成你实际跑通的模型名

    # 1. 实例化组件
    prompt = PromptTemplate("请用一句幽默的话，向小白解释什么是【{topic}】。")
    model = QwenLLM(SERVER_URL, MODEL)
    parser = KeywordsParser()  # <--- 新成员加入

    # 2. 奇迹发生的时刻：用 | 符号组装链条！
    chain = prompt | model | parser  # <--- 现在链条里有了三个组件，数据会依次流过它们

    # 3. 运行链条
    print("--- 🚀 开始运行链条 ---")
    final_output = await chain.ainvoke({"topic": "Python 里的异步编程"})

    print(f"\n✨ 最终解析结果:")
    print(f"💬 完整回复: {final_output['original_reply']}")
    print(f"🏷️ 提取标签: {final_output['keywords']}")


if __name__ == "__main__":
    asyncio.run(main())