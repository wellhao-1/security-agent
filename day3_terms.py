terms = [
    {"en": "Agent", "zh": "智能体", "desc": "能够根据目标执行任务的系统"},
    {"en": "Model", "zh": "模型", "desc": "用于处理输入并生成输出的核心模块"},
    {"en": "Prompt", "zh": "提示词", "desc": "用户提供给模型的输入指令"},
    {"en": "Task", "zh": "任务", "desc": "系统需要完成的具体工作"},
    {"en": "Workflow", "zh": "工作流", "desc": "完成任务的一系列步骤"},
    {"en": "Memory", "zh": "记忆", "desc": "系统保存上下文信息的能力"},
    {"en": "Tool", "zh": "工具", "desc": "智能体可以调用的外部功能"},
    {"en": "Retrieval", "zh": "检索", "desc": "从资料中查找相关内容"},
    {"en": "Generation", "zh": "生成", "desc": "模型根据输入输出答案的过程"},
    {"en": "Embedding", "zh": "嵌入", "desc": "把文本转换成向量表示的方法"},
    {"en": "RAG", "zh": "检索增强生成", "desc": "先检索资料再生成回答的方法"},
    {"en": "Router", "zh": "路由器", "desc": "判断问题该交给哪个模块处理"},
    {"en": "LLM", "zh": "大语言模型", "desc": "能够理解和生成自然语言的大模型"},
    {"en": "Context", "zh": "上下文", "desc": "当前对话或任务相关的信息环境"},
    {"en": "Token", "zh": "词元", "desc": "模型处理文本时使用的基本单位"}
]

print("=== 智能体术语表 ===")

for i, term in enumerate(terms, start=1):
    print(f"{i}. {term['en']} - {term['zh']}")
    print(f"   解释：{term['desc']}")


keyword = input("\n请输入你想查询的术语英文：").strip()

found = False
for term in terms:
    if term["en"].lower() == keyword.lower():
        print("\n查询结果：")
        print(f"{term['en']} - {term['zh']}")
        print(f"解释：{term['desc']}")
        found = True
        break

if not found:
    print("没有找到这个术语。")