# TODO: 实现主应用
from router import RuleRouter
from concept import ConceptExplainer
from advisor import StudyAdvisor
from web_search import WebSearchAgent
from rag import RAGPipeline
from utils import print_separator


class SecurityAgent:
    """
    信息安全学习助手 Agent。

    作用：
    接收用户问题
    ↓
    Router 分类
    ↓
    分发到不同模块
    ↓
    返回答案
    """

    def __init__(self):
        self.router = RuleRouter()

        self.concept_explainer = ConceptExplainer()

        self.study_advisor = StudyAdvisor()

        self.web_search_agent = WebSearchAgent()

        self.rag_pipeline = RAGPipeline(top_k=3)

    def build(self):
        """
        构建需要提前初始化的模块。

        当前主要是 RAG Retriever 索引。
        """

        print("[INFO] 正在构建 RAG 检索索引...")

        self.rag_pipeline.build()

        print("[INFO] Agent 初始化完成")

    def answer(self, question):
        """
        根据用户问题返回答案。
        """

        label = self.router.route(question)

        print(f"\n[ROUTER] 当前问题标签: {label}")

        if label == "concept_explanation":
            result = self.concept_explainer.answer(question)

            return {
                "label": label,
                "question": question,
                "answer": result["answer"],
                "detail": result
            }

        elif label == "rag_qa":
            result = self.rag_pipeline.answer(question)

            return {
                "label": label,
                "question": question,
                "answer": result["answer"],
                "detail": result
            }

        elif label == "study_advice":
            result = self.study_advisor.answer(question)

            return {
                "label": label,
                "question": question,
                "answer": result["answer"],
                "detail": result
            }

        elif label == "web_search":
            result = self.web_search_agent.answer(question)

            return {
                "label": label,
                "question": question,
                "answer": result["answer"],
                "detail": result
            }

        else:
            return {
                "label": label,
                "question": question,
                "answer": "暂不支持该类型问题。",
                "detail": {}
            }


def print_agent_result(result):
    """
    打印 Agent 回答结果。
    """

    print_separator("Agent 回答结果")

    print(f"\n问题: {result['question']}")
    print(f"标签: {result['label']}")

    print("\n回答:")
    print(result["answer"])


if __name__ == "__main__":
    agent = SecurityAgent()

    agent.build()

    while True:
        question = input("\n请输入你的问题，输入 q 退出：")

        if question.lower() == "q":
            print("已退出 Security Agent。")
            break

        result = agent.answer(question)

        print_agent_result(result)