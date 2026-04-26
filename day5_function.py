import json
# 术语表
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

def save_terms_to_json(filename):
    """把术语表保存为 JSON 文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=4)
    print(f"术语表已保存到 {filename}")

def load_terms_from_json(filename):
    """从 JSON 文件加载术语表"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 测试：保存术语表到 JSON 文件
save_terms_to_json("terms.json")

# 测试：加载术语表并打印
loaded_terms = load_terms_from_json("terms.json")
print(loaded_terms)