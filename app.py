from router import RuleRouter
from router_model import MLRouter
from concept import ConceptExplainer
from advisor import StudyAdvisor
from web_search import WebSearchAgent
from rag import RAGPipeline
from memory import ConversationMemory
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
    保存对话记忆
    ↓
    返回答案

    Day22 新增：
    优先使用机器学习版 MLRouter。
    如果 MLRouter 模型不存在，则自动退回 RuleRouter。
    """

    def __init__(self):
        # Day22：优先使用机器学习 Router
        self.router = MLRouter()

        # 如果模型没有成功加载，则退回规则 Router
        if self.router.model is None:
            print("[WARNING] MLRouter 不可用，自动切换到 RuleRouter")
            self.router = RuleRouter()

        self.concept_explainer = ConceptExplainer()

        self.study_advisor = StudyAdvisor()

        self.web_search_agent = WebSearchAgent()

        self.rag_pipeline = RAGPipeline(top_k=3)

        self.memory = ConversationMemory(max_turns=5)

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

        question = question.strip()

        if question == "":
            return {
                "label": "empty",
                "question": question,
                "answer": "请输入有效问题。",
                "detail": {},
                "memory_context": self.memory.get_context()
            }

        if question == "/memory":
            memory_text = self.memory.get_context()

            if memory_text == "":
                answer = "当前没有保存任何对话记忆。"
            else:
                answer = memory_text

            return {
                "label": "memory",
                "question": question,
                "answer": answer,
                "detail": {
                    "memory": self.memory.get_history()
                }
            }

        if question == "/clear":
            self.memory.clear()

            return {
                "label": "memory_clear",
                "question": question,
                "answer": "Memory 已清空。",
                "detail": {}
            }

        memory_context = self.memory.get_context()

        enhanced_question = self.memory.build_question_with_context(question)

        # Day22：这里的 self.router 可能是 MLRouter，也可能是 RuleRouter
        label = self.router.route(question)

        print(f"\n[ROUTER] 当前问题标签: {label}")

        if label == "concept_explanation":
            result = self.concept_explainer.answer(question)

        elif label == "rag_qa":
            result = self.rag_pipeline.answer(enhanced_question)

        elif label == "study_advice":
            result = self.study_advisor.answer(question)

        elif label == "web_search":
            result = self.web_search_agent.answer(question)

        else:
            result = {
                "question": question,
                "prompt": "",
                "answer": "暂不支持该类型问题。"
            }

        answer = result["answer"]

        self.memory.add_turn(
            user_question=question,
            assistant_answer=answer
        )

        return {
            "label": label,
            "question": question,
            "answer": answer,
            "detail": result,
            "memory_context": memory_context
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

        if question.lower().strip() == "q":
            print("已退出 Security Agent。")
            break

        result = agent.answer(question)

        print_agent_result(result)