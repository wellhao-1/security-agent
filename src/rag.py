from retriever import TfidfRetriever
from utils import print_separator
from llm import SimpleLLM


def build_rag_prompt(question, retrieved_chunks):
    """
    构建 RAG Prompt。

    参数：
    question: 用户问题
    retrieved_chunks: Retriever 返回的 top-k chunks

    返回：
    prompt: 拼接后的提示词
    """

    context_text = ""

    for idx, chunk in enumerate(retrieved_chunks):
        context_text += f"\n[资料 {idx + 1}]\n"
        context_text += f"来源文件: {chunk['filename']}\n"
        context_text += f"内容: {chunk['content']}\n"

    prompt = f"""
你是一个信息安全学习助手。

请你根据下面提供的资料回答用户问题。

要求：
1. 只根据资料回答，不要编造资料中没有的信息。
2. 回答要清晰、分点说明。
3. 如果资料不足，请说明“根据当前资料无法完整回答”。

资料：
{context_text}

用户问题：
{question}

请给出回答：
"""

    return prompt.strip()


class RAGPipeline:
    """
    RAG 问答管道。

    作用：
    用户输入问题
    ↓
    Retriever 检索相关 chunks
    ↓
    构建 Prompt
    ↓
    LLM 生成回答
    """

    def __init__(self, top_k=3):
        self.top_k = top_k

        self.retriever = TfidfRetriever()

        self.llm = SimpleLLM()

    def build(self):
        """
        构建 Retriever 索引。
        """

        self.retriever.build_index()

    def answer(self, question):
        """
        根据用户问题生成 RAG 回答。

        参数：
        question: 用户问题

        返回：
        result: 包含问题、检索结果、prompt、answer 的字典
        """

        retrieved_chunks = self.retriever.search(
            query=question,
            top_k=self.top_k
        )

        if len(retrieved_chunks) == 0:
            return {
                "question": question,
                "retrieved_chunks": [],
                "prompt": "",
                "answer": "没有检索到相关资料，无法回答。"
            }

        prompt = build_rag_prompt(
            question=question,
            retrieved_chunks=retrieved_chunks
        )

        answer = self.llm.generate(prompt)

        result = {
            "question": question,
            "retrieved_chunks": retrieved_chunks,
            "prompt": prompt,
            "answer": answer
        }

        return result


def print_rag_result(result):
    """
    打印 RAG 问答结果。
    """

    print_separator("RAG 问答结果")

    print(f"\n用户问题:\n{result['question']}")

    print_separator("检索到的资料")

    for idx, chunk in enumerate(result["retrieved_chunks"]):
        print(f"\n[{idx + 1}] 来源文件: {chunk['filename']}")
        print(f"相似度分数: {chunk['score']:.4f}")
        print(f"chunk_id: {chunk['chunk_id']}")
        print("\n内容:")
        print(chunk["content"][:300])
        print("\n" + "-" * 60)

    print_separator("最终 Prompt")

    print(result["prompt"])

    print_separator("最终回答")

    print(result["answer"])


if __name__ == "__main__":
    rag = RAGPipeline(top_k=3)

    rag.build()

    while True:
        question = input("\n请输入你的问题，输入 q 退出：")

        if question.lower() == "q":
            print("已退出 RAG 系统。")
            break

        result = rag.answer(question)

        print_rag_result(result)