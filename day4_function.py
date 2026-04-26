terms = {
    "agent": "智能体：能够根据目标执行任务的系统。",
    "model": "模型：用于处理输入并生成输出的核心模块。",
    "prompt": "提示词：用户提供给模型的输入指令。",
    "task": "任务：系统需要完成的具体工作。",
    "workflow": "工作流：完成任务的一系列步骤。",
    "memory": "记忆：系统保存上下文信息的能力。",
    "tool": "工具：智能体可以调用的外部功能。",
    "retrieval": "检索：从资料中查找相关内容。",
    "generation": "生成：模型根据输入输出答案的过程。",
    "embedding": "嵌入：把文本转换成向量表示的方法。",
    "rag": "检索增强生成：先检索资料，再结合资料生成回答的方法。",
    "router": "路由器：判断用户问题应该交给哪个模块处理。",
    "llm": "大语言模型：能够理解和生成自然语言的大模型。",
    "context": "上下文：当前对话或任务相关的信息环境。",
    "token": "词元：模型处理文本时使用的基本单位。"
}


def explain_term(term):
    """
    根据英文术语返回中文解释。
    """
    key = term.lower().strip()

    if key in terms:
        return terms[key]
    else:
        return "没有找到这个术语。"


def judge_question_type(question):
    """
    判断用户问题类型。
    这是后面 Router 模块的早期雏形。
    """
    question = question.strip()

    if "什么是" in question or "是什么意思" in question or "区别" in question or "定义" in question:
        return "concept_explanation"
    elif "根据资料" in question or "知识库" in question or "文档" in question:
        return "rag_qa"
    elif "怎么学" in question or "学习路线" in question or "入门" in question:
        return "study_advice"
    elif "最新" in question or "最近" in question or "互联网" in question or "搜索" in question:
        return "web_search"
    else:
        return "unknown"


print("=== Day 4 函数练习 ===")

user_term = input("请输入一个智能体相关英文术语：")
print(explain_term(user_term))

user_question = input("\n请输入一个问题：")
question_type = judge_question_type(user_question)

print("问题类型判断结果：", question_type)