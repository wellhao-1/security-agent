from llm import SimpleLLM


class WebSearchTool:
    """
    联网搜索工具模拟版。

    对应 Router 标签：
    web_search

    当前版本不真正联网，
    只是模拟搜索结果。
    """

    def search(self, query):
        """
        模拟搜索结果。
        """

        print(f"[WEB SEARCH] 模拟联网搜索: {query}")

        results = [
            {
                "title": "近期高危漏洞通报示例",
                "snippet": "近期多个系统出现远程代码执行、权限绕过等高危漏洞，建议及时关注官方安全公告。"
            },
            {
                "title": "安全事件示例",
                "snippet": "某些攻击活动利用弱口令、钓鱼邮件和未修复漏洞进行入侵，企业应加强补丁管理。"
            },
            {
                "title": "CVE 漏洞信息示例",
                "snippet": "CVE 编号用于标识公开披露的安全漏洞，分析漏洞时应关注影响范围、利用条件和修复方案。"
            }
        ]

        return results


def build_web_search_prompt(question, search_results):
    """
    构建联网搜索总结 Prompt。
    """

    context = ""

    for idx, item in enumerate(search_results):
        context += f"\n[搜索结果 {idx + 1}]\n"
        context += f"标题: {item['title']}\n"
        context += f"摘要: {item['snippet']}\n"

    prompt = f"""
你是一个信息安全助手。

请根据下面的搜索结果，回答用户问题。

要求：
1. 说明这是基于搜索结果的总结。
2. 不要编造搜索结果中没有的信息。
3. 回答要清晰、分点说明。
4. 如果信息不足，请提醒用户需要进一步查证。

搜索结果：
{context}

用户问题：
{question}

请给出回答：
"""

    return prompt.strip()


class WebSearchAgent:
    """
    搜索问答模块。

    流程：
    用户问题
    ↓
    WebSearchTool.search()
    ↓
    构建搜索总结 Prompt
    ↓
    LLM 生成回答
    """

    def __init__(self):
        self.search_tool = WebSearchTool()
        self.llm = SimpleLLM()

    def answer(self, question):
        search_results = self.search_tool.search(question)

        prompt = build_web_search_prompt(
            question=question,
            search_results=search_results
        )

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "search_results": search_results,
            "prompt": prompt,
            "answer": answer
        }


if __name__ == "__main__":
    agent = WebSearchAgent()

    result = agent.answer("最近有哪些高危漏洞？")

    print(result["answer"])