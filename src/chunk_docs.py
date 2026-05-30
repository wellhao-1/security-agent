import os
import json

from src.load_docs import load_documents
from src.utils import print_separator


def chunk_text(text, chunk_size=300, overlap=50):
    """
    将一段长文本切成多个小块。

    参数：
    text: 原始文本
    chunk_size: 每个 chunk 的最大字符数
    overlap: 相邻 chunk 之间重叠的字符数

    返回：
    chunks: 文本块列表
    """

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

        if start >= text_length:
            break

    return chunks


def chunk_documents(documents, chunk_size=300, overlap=50):
    """
    将所有文档切块。

    参数：
    documents: load_documents() 返回的文档列表

    返回：
    all_chunks: 所有文档块列表
    """

    all_chunks = []

    chunk_id = 0

    for doc in documents:
        filename = doc["filename"]
        content = doc["content"]

        chunks = chunk_text(
            text=content,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for index, chunk in enumerate(chunks):
            chunk_obj = {
                "chunk_id": chunk_id,
                "filename": filename,
                "chunk_index": index,
                "content": chunk,
                "length": len(chunk)
            }

            all_chunks.append(chunk_obj)

            chunk_id += 1

    return all_chunks


def save_chunks(chunks, output_path="../processed_data/chunks.json"):
    """
    将 chunks 保存为 JSON 文件。
    """

    output_dir = os.path.dirname(output_path)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"\n[SUCCESS] chunks 已保存到: {output_path}")


def print_chunks_summary(chunks):
    """
    打印 chunks 统计信息。
    """

    print_separator("Chunking 结果")

    print(f"\n总 chunk 数量: {len(chunks)}")

    if len(chunks) == 0:
        print("[WARNING] 没有生成任何 chunk")
        return

    total_length = sum(
        chunk["length"] for chunk in chunks
    )

    avg_length = total_length / len(chunks)

    print(f"总字符数: {total_length}")
    print(f"平均 chunk 长度: {avg_length:.2f}")

    longest_chunk = max(
        chunks,
        key=lambda x: x["length"]
    )

    print("\n最长 chunk:")
    print(f"chunk_id: {longest_chunk['chunk_id']}")
    print(f"来源文件: {longest_chunk['filename']}")
    print(f"长度: {longest_chunk['length']}")

    print_separator("Chunk 预览")

    for chunk in chunks[:5]:
        print(f"\nchunk_id: {chunk['chunk_id']}")
        print(f"来源文件: {chunk['filename']}")
        print(f"文档内编号: {chunk['chunk_index']}")
        print(f"长度: {chunk['length']}")

        print("\n内容预览:")
        print(chunk["content"][:150])

        print("\n" + "-" * 60)


if __name__ == "__main__":
    documents = load_documents()

    chunks = chunk_documents(
        documents=documents,
        chunk_size=300,
        overlap=50
    )

    print_chunks_summary(chunks)

    save_chunks(chunks)