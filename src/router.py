# TODO: 实现路由器模块
class RuleRouter:
    """
    规则版 Router。

    作用：
    根据用户问题判断应该走哪个模块。

    支持四类标签：
    - concept_explanation
    - rag_qa
    - study_advice
    - web_search
    """

    def __init__(self):
        self.labels = [
            "concept_explanation",
            "rag_qa",
            "study_advice",
            "web_search"
        ]

    def route(self, question):
        """
        根据用户问题返回分类标签。
        """

        q = question.strip().lower()

        # 1. 联网搜索类
        web_keywords = [
            "最新",
            "最近",
            "今天",
            "当前",
            "新闻",
            "高危漏洞",
            "cve",
            "0day",
            "漏洞通报",
            "安全事件"
        ]

        for keyword in web_keywords:
            if keyword.lower() in q:
                return "web_search"

        # 2. RAG 知识库问答类
        rag_keywords = [
            "根据资料",
            "根据文档",
            "根据知识库",
            "结合资料",
            "结合文档",
            "从资料中",
            "基于资料",
            "基于知识库"
        ]

        for keyword in rag_keywords:
            if keyword.lower() in q:
                return "rag_qa"

        # 3. 学习建议类
        advice_keywords = [
            "怎么学",
            "如何学习",
            "学习路线",
            "学习规划",
            "入门",
            "新手",
            "初学者",
            "应该怎么开始",
            "推荐学习"
        ]

        for keyword in advice_keywords:
            if keyword.lower() in q:
                return "study_advice"

        # 4. 概念解释类
        concept_keywords = [
            "什么是",
            "解释",
            "介绍",
            "定义",
            "原理",
            "区别",
            "作用",
            "含义"
        ]

        for keyword in concept_keywords:
            if keyword.lower() in q:
                return "concept_explanation"

        # 默认走概念解释
        return "concept_explanation"


if __name__ == "__main__":
    router = RuleRouter()

    test_questions = [
        "什么是 SQL 注入？",
        "根据资料解释 HTTPS 的工作流程",
        "Web 安全怎么学？",
        "最近有哪些高危漏洞？"
    ]

    for question in test_questions:
        label = router.route(question)
        print(question, "=>", label)