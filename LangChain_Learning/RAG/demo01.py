import os
from datetime import datetime
from langchain_core.documents import Document
from langchain_classic.document_loaders.base import BaseLoader


class SimpleQALoader(BaseLoader):
    """
    简单的问答文件加载器

    该加载器用于从文本文件中加载问答对，文件格式要求每两行为一组，
    第一行为问题(Q)，第二行为答案(A)

    Args:
        file_path (str): 问答文件的路径
        time_fmt (str): 时间格式字符串，默认为 "%Y-%m-%d %H:%M:%S"
    """

    def __init__(self, file_path: str, time_fmt: str = "%Y-%m-%d %H:%M:%S"):
        self.file_path = file_path
        self.time_fmt = time_fmt

    def load(self):
        """
        加载并解析问答文件

        读取文件中的问答对，每两行构成一个问答文档，第一行为问题，第二行为答案。
        每个文档包含问题和答案的组合内容，以及文件的元数据信息。

        Returns:
            list[Document]: 包含问答内容的文档列表，每个文档包含page_content和metadata
        """
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        docs = []
        created_ts = os.path.getctime(self.file_path)
        created_at = datetime.fromtimestamp(created_ts).strftime(self.time_fmt)

        # 每两行构成一个 Q/A
        for i in range(0, len(lines), 2):
            q = lines[i].lstrip("Q：:").strip()
            a = lines[i + 1].lstrip("A：:").strip()
            page_content = f"Q: {q}\nA: {a}"

            doc = Document(
                page_content=page_content,
                metadata={
                    "source": self.file_path,
                    "created_at": created_at,
                }
            )
            docs.append(doc)

        return docs


# 使用示例
if __name__ == "__main__":
    loader = SimpleQALoader("faq.txt")
    docs = loader.load()
    print(f"共解析到 {len(docs)} 个文档")
    for i, d in enumerate(docs, 1):
        print(f"\n--- 文档 {i} ---")
        print(d.page_content)
        print("元数据：", d.metadata)