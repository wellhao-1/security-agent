import os

from dotenv import load_dotenv
from tavily import TavilyClient

from src.llm import SimpleLLM


load_dotenv()


class WebSearchTool:
    """
    真实联网搜索工具。

    当前使用 Tavily Search API。
    """

    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")

        if not self.api_key:
            raise ValueError(
                "未找到 TAVILY_API_KEY，请在项目根目录 .env 文件中配置。"
            )

        self.client = TavilyClient(
            api_key=self.api_key
        )

    def search(self, query, max_results=5):
        """
        执行真实联网搜索。

        参数：
        query: 用户问题
        max_results: 返回搜索结果数量

        返回：
        results: 搜索结果列表
        """

        try:
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=max_results
            )

            raw_results = response.get("results", [])

            results = []

            for item in raw_results:
                result = {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("content", ""),
                    "score": item.get("score", 0)
                }

                results.append(result)

            return results

        except Exception as e:
            print(f"[WEB SEARCH ERROR] Tavily 搜索失败：{e}")
            return []


def build_web_search_prompt(question, search_results):
    """
    构建联网搜索总结 Prompt。
    """

    if len(search_results) == 0:
        prompt = f"""
你是一个信息安全助手。

用户问题：
{question}

当前没有成功获取到联网搜索结果。

请告诉用户：
1. 当前无法基于实时搜索结果回答。
2. 可以稍后重试。
3. 如果是安全事件或漏洞信息，建议以官方公告、CVE、厂商安全通告为准。
"""
        return prompt.strip()

    context = ""

    for idx, item in enumerate(search_results):
        context += f"\n[搜索结果 {idx + 1}]\n"
        context += f"标题: {item['title']}\n"
        context += f"链接: {item['url']}\n"
        context += f"摘要: {item['snippet']}\n"
        context += f"相关性分数: {item['score']}\n"

    prompt = f"""
你是一个信息安全助手。

请根据下面的真实联网搜索结果回答用户问题。

要求：
1. 明确说明答案基于联网搜索结果。
2. 不要编造搜索结果中没有的信息。
3. 回答要清晰、分点说明。
4. 如果信息不足，请提醒用户进一步查证。
5. 尽量保留重要来源链接。
6. 如果涉及漏洞、CVE、安全事件，请提醒用户以官方公告为准。

联网搜索结果：
{context}

用户问题：
{question}

请给出回答：
"""

    return prompt.strip()


class WebSearchAgent:
    """
    搜索问答模块。

    对应 Router 标签：
    web_search

    流程：
    用户问题
    ↓
    Tavily 搜索
    ↓
    构建搜索 Prompt
    ↓
    智谱 GLM 总结回答
    """

    def __init__(self):
        self.search_tool = WebSearchTool()
        self.llm = SimpleLLM()

    def answer(self, question):
        search_results = self.search_tool.search(
            query=question,
            max_results=5
        )

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