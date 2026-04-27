class Agent:
    def __init__(self,name,role):
        self.name=name
        self.role=role

    def introduce(self):
        return f"我是{self.name},我的角色是{self.role}"

    def classify_question(self, question):
        """
        这是一个最简单的问题分类函数。
        后面我们会把它升级成 Router，再升级成自训练分类器。
        """

        if "什么是" in question or "定义" in question or "解释" in question:
            return "concept_explanation"

        elif "根据资料" in question or "文档" in question or "知识库" in question:
            return "rag_qa"

        elif "怎么学" in question or "学习路线" in question or "入门" in question:
            return "study_advice"

        elif "最新" in question or "最近" in question or "搜索" in question:
            return "web_search"

        else:
            return "concept_explanation"

    def response(self, question):
        question_type = self.classify_question(question)
        if question_type == "concept_explanation":
            return f"问题类型：概念解释。你问的是：{question}"

        elif question_type == "rag_qa":
            return f"问题类型：资料库问答。之后我会从本地知识库中检索资料来回答：{question}"

        elif question_type == "study_advice":
            return f"问题类型：学习建议。之后我会为你生成学习路线：{question}"

        elif question_type == "web_search":
            return f"问题类型：联网搜索。之后可以接入搜索工具处理：{question}"

        else:
            return "暂时无法判断问题类型。"

def main():
        agent=Agent(
            name="Security Learning Agent",
            role="信息安全学习助手"
        )

        print(agent.introduce())
        print("你可以输入一个信息安全相关问题，输入q结束。")
        while True:
          try:
            question = input("\n请输入问题：")
            if question == "q":
                print("程序结束")
                break
            answer=agent.response(question)
            print(answer)
          except Exception as e:
              print(f"程序错误了哦：{e}")

if __name__ == "__main__":
    main()