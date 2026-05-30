# TODO: 实现记忆模块
from src.utils import print_separator
class ConversationMemory:
    def __init__(self,max_turns=5):
        self.max_turns=max_turns
        self.history=[]

    def add_message(self,role,content):
        """
                添加一条对话记录。

                role:
                - user
                - assistant

                content:
                消息内容
                """
        message={
            "role":role,
            "content":content
        }
        self.history.append(message)
        self._trim_history()

    def add_turn(self,user_question,assistant_answer):
        """添加一轮玩整对话"""
        self.add_message("user",user_question)
        self.add_message("assistant",assistant_answer)

    def _trim_history(self):
        """
               只保留最近 max_turns 轮对话。

               一轮对话包含：
               user + assistant

               所以最多保留 max_turns * 2 条消息。
               """
        max_message=self.max_turns*2

        if len(self.history)>max_message:
            self.history=self.history[-max_message:]

    def get_history(self):
        """获取对话历史"""
        return self.history

    def get_context(self):
        """将历史记录拼接成上下文"""

        if len(self.history)==0:
            return ""

        context=""

        for message in self.history:
            role=message["role"]
            content=message["content"]
            if role=="user":
                context+=f"用户：{content}\n"
            elif role=="assistant":
                context+=f"助手：{content}\n"

        return  context.strip()

    def get_last_question(self):
        """获取最后一条用户问题"""

        for message in reversed(self.history):
            if message["role"]=="user":
                return message["content"]
        return ""

    def rewrite_question(self, question, llm):
        """
        使用 LLM 将当前问题结合历史对话改写成独立问题。

        作用：
        解决多轮对话中的省略和指代问题。

        例如：
        历史：用户问过“什么是 SQL 注入？”
        当前问题：“那怎么防御？”
        改写后：“SQL 注入怎么防御？”
        """

        context = self.get_context()

        if context == "":
            return question

        prompt = f"""
    你是一个问题改写助手。

    请根据对话历史，将当前用户问题改写成一个语义完整、可以独立理解的问题。

    要求：
    1. 不要回答问题。
    2. 只输出改写后的问题。
    3. 如果当前问题已经完整，直接原样输出。
    4. 不要添加无关信息。
    5. 保留用户原本的提问意图。

    对话历史：
    {context}

    当前用户问题：
    {question}

    改写后的问题：
    """

        rewritten_question = llm.generate(prompt)

        return rewritten_question.strip()

    def build_question_with_context(self,question):
        """
        构建带有上下文的问题。
        当前版本仅为简单拼接，不改写
        参数：
        question: 用户问题
        返回：
        带有上下文的问题
        """
        context=self.get_context()

        if context=="":
            return question

        enhanced_question=f"""下面是最近的历史对话：{context}
                               当前用户问题：{question}"""

        return enhanced_question.strip()

    def clear(self):
        """清空对话历史"""
        self.history=[]

    def print_memory(self):
        """打印当前记忆内容"""

        print_separator("当前Memory内容")

        if len(self.history)==0:
            print("暂无对话记忆")
            return

        for idx , message in enumerate(self.history):
            print(f"[{idx+1}] {message['role']}")
            print(message["content"][:300])

