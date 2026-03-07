import re
import json
from pathlib import Path
from datetime import datetime, timezone

def clean_text(text: str) -> str:
    """
    清洗文本内容，去除HTML标签和多余空格及无效字符。

    参数:
        text (str): 需要清洗的原始文本。

    返回:
        str: 清洗后的文本内容。
    """
    # 去掉 HTML 标签（如果有残留）
    text = re.sub(r"<.*?>", "", text)
    # 去掉多余空格并过滤空行
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def split_faq(text: str):
    """
    根据 Q/A 规则将FAQ文本切分为问题和答案对。

    参数:
        text (str): 包含FAQ内容的文本字符串。

    返回:
        list[dict]: 每个元素是一个包含"question"和"answer"键的字典。
    """
    # 按 Q： 或 Q: 分割文本
    parts = re.split(r"(?:^|\n)Q[:：]", text)
    qa_pairs = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # 将第一行作为问题，其余部分作为答案
        lines = part.splitlines()
        question = lines[0]
        answer = "\n".join(lines[1:]) if len(lines) > 1 else ""
        qa_pairs.append({
            "question": question,
            "answer": answer
        })
    return qa_pairs

def process_faq(input_file: str, output_file: str, source_url: str, category="FAQ"):
    """
    处理FAQ文本文件，清洗、分割并添加元数据后保存为JSON格式。

    参数:
        input_file (str): 输入的原始FAQ文本文件路径。
        output_file (str): 输出处理后的JSON文件路径。
        source_url (str): 数据来源URL。
        category (str): FAQ分类，默认为"FAQ"。

    返回:
        None
    """
    raw_text = Path(input_file).read_text(encoding="utf-8")
    cleaned_text = clean_text(raw_text)
    qa_pairs = split_faq(cleaned_text)

    # 添加元数据信息
    now = datetime.now(timezone.utc).isoformat()
    processed = []
    for qa in qa_pairs:
        processed.append({
            "question": qa["question"],
            "answer": qa["answer"],
            "metadata": {
                "source": source_url,
                "category": category,
                "crawl_time": now
            }
        })

    Path(output_file).write_text(
        json.dumps(processed, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ 已处理 {len(processed)} 条 FAQ，结果保存到 {output_file}")

if __name__ == "__main__":
    process_faq(
        input_file="faq.txt",
        output_file="faq_processed.json",
        source_url="https://waimai.meituan.com/help/faq",
        category="支付问题"
    )