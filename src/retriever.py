# TODO: 实现检索器模块
import os
import  json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils import print_separator

def load_chunks(chunk_path="processed_data/chunks.json"):
    """
       读取 Day17 生成的 chunks.json。

       参数：
       chunks_path: chunks.json 文件路径

       返回：
       chunks: chunk 列表
       """

    if not os.path.exists(chunk_path):
        print(f"[ERROR]chunks文件不存在：{chunk_path}")
        return []

    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks=json.load(f)

    return chunks

class TfidfRetriever:
    """
       基于 TF-IDF 的简单检索器。

       作用：
       输入用户问题
       从 chunks 中找出最相关的 top-k 文本块
       """
    def __init__(self, chunk_path="processed_data/chunks.json"):
        self.chunk_path=chunk_path
        self.chunks=[]
        self.vectorizer=None
        self.chunk_matrix=None

    def build_index(self):
        """
               构建检索索引。

               主要做三件事：
               1. 读取 chunks
               2. 提取 chunk 内容
               3. 用 TF-IDF 向量化
               """

        self.chunks=load_chunks(self.chunk_path)

        if len(self.chunks)==0:
            print("[ERROR]没有找到任何chunk")
            return

        texts=[
            chunk["content"] for chunk in self.chunks
        ]

        self.vectorizer=TfidfVectorizer(
            analyzer="char",
            ngram_range=(2,4),
        )

        self.chunk_matrix=self.vectorizer.fit_transform(texts)

        print(f"[SUCCESS]Retriever索引构建完毕，共{len(self.chunks)}个chunks")

    def search(self, query, top_k=3):
        """
        根据用户问题检索最相关的 top-k chunks。

        参数：
        query: 用户问题
        top_k: 返回几个最相关文本块

        返回：
        results: 检索结果列表
        """

        if self.vectorizer is None or self.chunk_matrix is None:
            print("[ERROR]请先构建索引")
            return []

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.chunk_matrix
        )[0]

        ranked_indices = scores.argsort()[::-1]

        results = []

        for idx in ranked_indices[:top_k]:
            chunk = self.chunks[idx]

            result = {
                "score": float(scores[idx]),
                "chunk_id": chunk["chunk_id"],
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                "length": chunk["length"]
            }

            results.append(result)

        return results

def print_search_results(query, results):
    """
    打印检索结果。
    """

    print_separator("Retriever 检索结果")

    print(f"\n用户问题: {query}")
    print(f"返回结果数量: {len(results)}")

    for idx, result in enumerate(results):
        print("\n" + "-" * 60)

        print(f"排名: {idx + 1}")
        print(f"相似度分数: {result['score']:.4f}")
        print(f"chunk_id: {result['chunk_id']}")
        print(f"来源文件: {result['filename']}")
        print(f"文档内编号: {result['chunk_index']}")
        print(f"长度: {result['length']}")

        print("\n内容:")
        print(result["content"][:300])

if __name__ == "__main__":
    retriever = TfidfRetriever()

    retriever.build_index()

    while True:
        query = input("\n请输入你的问题，输入 q 退出：")

        if query.lower() == "q":
            print("已退出 Retriever 测试。")
            break

        results = retriever.search(
            query=query,
            top_k=3
        )

        print_search_results(query, results)