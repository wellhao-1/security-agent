# TODO: 实现安全顾问模块
from src.llm import SimpleLLM


def build_advice_prompt(question):
    """
    构建学习建议 Prompt。
    """

    prompt = f"""
你是一个信息安全学习规划助手。

请根据用户的问题，给出清晰的学习建议。

要求：
1. 按阶段给出学习路线。
2. 每个阶段说明学习重点。
3. 给出适合初学者的实践建议。
4. 回答要具体，不要空泛。

用户问题：
{question}

请给出学习建议：
"""

    return prompt.strip()


class StudyAdvisor:
    """
    学习建议模块。

    对应 Router 标签：
    study_advice
    """

    def __init__(self):
        self.llm = SimpleLLM()

    def answer(self, question):
        prompt = build_advice_prompt(question)

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "prompt": prompt,
            "answer": answer
        }


if __name__ == "__main__":
    advisor = StudyAdvisor()

    result = advisor.answer("Web 安全怎么学？")

    print(result["answer"])