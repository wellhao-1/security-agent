from src.llm import SimpleLLM


def build_concept_prompt(question):
    """
    构建概念解释 Prompt。
    """

    prompt = f"""
你是一个信息安全学习助手。

请用适合初学者理解的方式解释下面的问题。

要求：
1. 先给出简明定义。
2. 再解释基本原理。
3. 最后给一个简单例子。
4. 回答要清晰，不要太复杂。

用户问题：
{question}

请给出解释：
"""

    return prompt.strip()


class ConceptExplainer:
    """
    概念解释模块。

    对应 Router 标签：
    concept_explanation
    """

    def __init__(self):
        self.llm = SimpleLLM()

    def answer(self, question):
        prompt = build_concept_prompt(question)

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "prompt": prompt,
            "answer": answer
        }


if __name__ == "__main__":
    explainer = ConceptExplainer()

    result = explainer.answer("什么是 SQL 注入？")

    print(result["answer"])