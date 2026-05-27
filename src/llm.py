import os
import requests

from dotenv import load_dotenv


load_dotenv()

class SimpleLLM:
    """
    真实 LLM 调用模块。

    当前使用智谱 AI GLM API。
    为了兼容项目其他模块，类名仍然保留为 SimpleLLM。

    """

    def __init__(self):
        self.api_key = os.getenv("ZHIPU_API_KEY")
        self.model = os.getenv("ZHIPU_MODEL", "glm-5.1")
        self.api_base = os.getenv(
            "ZHIPU_API_BASE",
            "https://open.bigmodel.cn/api/paas/v4"
        )

        if not self.api_key:
            raise ValueError(
                "未找到 ZHIPU_API_KEY，请在项目根目录 .env 文件中配置。"
            )

        self.chat_url = f"{self.api_base}/chat/completions"

    def generate(self, prompt, temperature=0.7):
        """
        调用智谱 GLM API，根据 prompt 生成回答。

        参数：
        prompt: 用户输入或系统构造好的 Prompt
        temperature: 控制回答随机性，越高越发散

        返回：
        answer: 模型回答文本
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业、严谨的信息安全学习助手。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(
                self.chat_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            answer = data["choices"][0]["message"]["content"]

            return answer.strip()

        except requests.exceptions.RequestException as e:
            return f"[LLM ERROR] 智谱 API 请求失败：{e}"

        except KeyError:
            return f"[LLM ERROR] 智谱 API 返回格式异常：{response.text}"

        except Exception as e:
            return f"[LLM ERROR] 未知错误：{e}"


if __name__ == "__main__":
    llm = SimpleLLM()

    result = llm.generate("请简单解释什么是 SQL 注入。")

    print(result)