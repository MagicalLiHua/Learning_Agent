from pathlib import Path
from typing import List
from transformers import AutoTokenizer
from PyPDF2 import PdfReader


class DocumentLoader:
    """
    文档加载器类，用于加载不同格式的文档内容。
    支持的格式包括：txt、pdf、md。
    """

    @staticmethod
    def load_txt(file_path: str) -> str:
        """
        加载文本文件内容。

        参数:
            file_path (str): 文本文件的路径。

        返回:
            str: 文件中的文本内容。
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def load_pdf(file_path: str) -> str:
        """
        加载 PDF 文件内容。

        参数:
            file_path (str): PDF 文件的路径。

        返回:
            str: 提取的 PDF 文本内容，各页之间以换行符连接。
        """
        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)

    @staticmethod
    def load_md(file_path: str) -> str:
        """
        加载 Markdown 文件内容。当前实现与加载 txt 文件相同。

        参数:
            file_path (str): Markdown 文件的路径。

        返回:
            str: 文件中的文本内容。
        """
        return DocumentLoader.load_txt(file_path)

    @staticmethod
    def load_document(file_path: str) -> str:
        """
        根据文件扩展名自动选择加载方法，加载对应格式的文档内容。

        参数:
            file_path (str): 文档文件的路径。

        返回:
            str: 加载的文档文本内容。

        异常:
            ValueError: 当文件格式不被支持时抛出。
        """
        ext = Path(file_path).suffix.lower()
        if ext == ".txt":
            return DocumentLoader.load_txt(file_path)
        elif ext == ".pdf":
            return DocumentLoader.load_pdf(file_path)
        elif ext == ".md":
            return DocumentLoader.load_md(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")


class QwenTextSplitter:
    """
    基于指定模型的 tokenizer 对文本进行切分的工具类。

    属性:
        tokenizer: 使用的分词器对象。
    """

    def __init__(self, model_name: str = "Qwen/Qwen2.5-7B"):
        """
        初始化分词器。

        参数:
            model_name (str): 用于加载 tokenizer 的模型名称，默认为 "Qwen/Qwen2.5-7B"。
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    def count_tokens(self, text: str) -> int:
        """
        计算文本的 token 数量。

        参数:
            text (str): 输入文本。

        返回:
            int: 文本的 token 数量。
        """
        return len(self.tokenizer.encode(text))

    def split_by_tokens(self, text: str, max_tokens: int = 500, overlap: int = 50) -> List[str]:
        """
        将文本按照最大 token 数量进行切分，并允许设置重叠 token 数量。

        参数:
            text (str): 待切分的文本。
            max_tokens (int): 每个片段的最大 token 数量，默认为 500。
            overlap (int): 片段之间的 token 重叠数，默认为 50。

        返回:
            List[str]: 切分后的文本片段列表。
        """
        tokens = self.tokenizer.encode(text)
        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + max_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            start += max_tokens - overlap
        return chunks


if __name__ == "__main__":
    # 加载示例文档
    file_path = "example.md"
    text = DocumentLoader.load_document(file_path)

    # 初始化文本切分器并统计原始 token 数量
    splitter = QwenTextSplitter(model_name="Qwen/Qwen3-14B")  # 模型名要和 HF 对应
    print("原始 Token 数:", splitter.count_tokens(text))

    # 按 token 切分文本
    chunks = splitter.split_by_tokens(text, max_tokens=300, overlap=50)
    print("按 Token 切分:", len(chunks), "块")
    print("第一块示例:\n", chunks[0][:200], "...")
