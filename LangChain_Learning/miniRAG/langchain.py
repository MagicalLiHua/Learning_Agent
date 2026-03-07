from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# 刚才测试用的语料
corpus = (
    "在深度学习中，Transformer架构是革命性的。"
    "它能够进行全局依赖建模，捕捉长距离的上下文关系，这使得它在自然语言处理任务中表现出色。"
    "transformer的核心是自注意力机制，它允许模型在处理输入时动态地关注不同部分的信息。"
    "与传统的RNN和CNN不同，Transformer能够并行处理整个输入序列，这大大加快了训练速度。"
    "Transformer架构的成功使得它成为了许多预训练语言模型（如BERT和GPT）的基础。"
    "Transformer的设计使得它在处理长文本时表现优异，因为它能够捕捉到更广泛的上下文信息。"
    "Transformer的自注意力机制使得模型能够更好地理解输入数据的结构和语义，从而提升了各种自然语言处理任务的性能。"
    "它完全抛弃了RNN和CNN，仅依赖自注意力机制来计算输入和输出的表示。"
    "这种设计使得模型在训练时高度可并行化，极大地提升了效率。"
)

# 1. 工业级切分 (对比你写的 overlap_text_splitter)
# 它按 separators 数组的优先级降级切分，最大限度保证句子完整
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=30,
    chunk_overlap=10,
    separators=["\n\n", "\n", "。", "，", " ", ""]
)
docs = text_splitter.create_documents([corpus])

# 2. 向量化与存储 (对比你写的 get_embedding + numpy 数组)
embeddings = OllamaEmbeddings(model="nomic-embed-text",
                              base_url="http://10.160.108.2:11434")
vector_store = FAISS.from_documents(docs, embeddings)

# 3. 实例化检索器 (对比你写的 retrieve_top_k)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 打印看看 LangChain 封装的 Document 对象
print(f"切分得到了 {len(docs)} 个 Chunk。")
for i, doc in enumerate(docs):
    print(f"Chunk {i+1}: {doc.page_content[:50]}...")  # 只打印前50个字符

# 测试检索效果
question = "Transformer架构的优势是什么？"
context = retriever.invoke(question)
print("\n检索结果：")
for i, doc in enumerate(context):
    print(f"Result {i+1}: {doc.page_content[:50]}...")  # 只打印前50个字符


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

# 准备 LLM 和 Prompt
llm = ChatOllama(model="qwen3-vl:8b", base_url="http://10.160.108.2:11434")

prompt = ChatPromptTemplate.from_template("""
请仅根据以下提供的上下文信息回答问题。如果不知道，请直接回答“我不知道”。
上下文信息:
{context}

问题: {question}
请使用下面的语言回答：{language}
""")

# 辅助函数：将检索到的多个 Document 对象拼接成纯文本字符串
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
        {
            # 先提取纯文本问题，再传给检索器，最后格式化文档
            "context": (lambda x: x["question"]) | retriever | format_docs,

            # 提取纯文本问题，传给 prompt 中的 {question}
            "question": lambda x: x["question"],

            # 提取语言要求，传给 prompt 中的 {language}
            "language": lambda x: x["language"]
        }
        | prompt
        | llm
        | StrOutputParser()
)

# 测试运行
print(rag_chain.invoke({"question": "Transformer架构的优势是什么？", "language": "English"}))