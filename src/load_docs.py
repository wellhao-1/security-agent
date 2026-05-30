# TODO: 实现文档加载模块
import os

from src.utils import print_separator

def load_documents(data_dir="../data"):

    documents = []
    # 检查目录是否存在
    if not os.path.exists(data_dir):

        print(f"[ERROR] 目录不存在: {data_dir}")

        return documents

    # 获取目录文件（排序）
    filenames = sorted(os.listdir(data_dir))

    # 遍历文件
    for filename in filenames:

        # 只读取 txt
        if filename.endswith(".txt"):

            file_path = os.path.join(data_dir, filename)

            try:

                # 打开文件
                with open(file_path, "r", encoding="utf-8") as f:

                    content = f.read()

                    # 去除首尾空格
                    content = content.strip()

                    # 构造文档对象
                    document = {
                        "filename": filename,
                        "content": content,
                        "length": len(content)
                    }

                    documents.append(document)

            except Exception as e:

                print(f"[ERROR] 文件读取失败: {filename}")
                print(e)

    # 空文档检查
    if len(documents) == 0:

        print("[WARNING] 未发现 txt 文档")

    return documents


def print_documents(documents):

    print_separator("知识库加载结果")

    print(f"\n成功加载文档数量: {len(documents)}")

    # 统计总字符数
    total_length = sum(
        doc["length"] for doc in documents
    )

    print(f"知识库总字符数: {total_length}")

    # 平均长度
    if len(documents) > 0:

        avg_length = total_length / len(documents)

        print(f"平均文档长度: {avg_length:.2f}")

    # 最长文档
    if len(documents) > 0:

        longest_doc = max(
            documents,
            key=lambda x: x["length"]
        )

        print("\n最长文档:")
        print(f"文件名: {longest_doc['filename']}")
        print(f"长度: {longest_doc['length']}")

    print_separator("文档预览")

    # 文档预览
    for idx, doc in enumerate(documents):

        print(f"\n[{idx+1}] 文件名: {doc['filename']}")

        print(f"字符数: {doc['length']}")

        preview = doc["content"][:120]

        print("\n内容预览:")

        print(preview)

        print("\n" + "-" * 60)


if __name__ == "__main__":

    docs = load_documents()
    print_documents(docs)