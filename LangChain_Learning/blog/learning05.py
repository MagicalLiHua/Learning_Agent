from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# 几个示例，说明模型该如何输出
examples = [
    {"input": "北京下雨吗", "output": "北京"},
    {"input": "上海热吗", "output": "上海"},
]

# 定义如何格式化每个示例
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="输入：{input}\n输出：{output}"
)

# 构建 FewShotPromptTemplate
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="按提示的格式，输出内容",
    suffix="输入：{input}\n输出：",  # 要放在示例后面的提示模板字符串。
    input_variables=["input"]  # 传入的变量
)

# 生成最终的 prompt
print(few_shot_prompt.format(input="天津今天刮风吗"))
