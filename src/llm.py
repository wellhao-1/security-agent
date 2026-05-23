class SimpleLLM:
    """
    简易 LLM 模拟器。

    现在还没有接真实大模型 API，
    所以这里先模拟 LLM 的生成过程。
    """

    def generate(self, prompt):
        answer = f"""
【模拟 LLM 回答】

我已经接收到 Prompt，并根据 Prompt 生成回答。

当前 Prompt 内容如下：

{prompt}
"""
        return answer.strip()
# TODO: 实现LLM模块
