# TODO: 实现路由分类器模型
import os
from cProfile import label

import  joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models/router_model.pkl')

class MLRouter:
    """
        机器学习版 Router。

        使用 TF-IDF + SVM 模型预测用户问题类别。

        支持标签：
        - concept_explanation
        - rag_qa
        - study_advice
        - web_search
    """
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path
        self.model=None
        self.load_model()

    def load_model(self):
        """
            加载模型。
        """
        if not os.path.exists(self.model_path):
            print("模型不存在，请先训练模型。")
            return
        self.model = joblib.load(self.model_path)
        print(f"模型加载成功：{self.model_path}")

    def route(self,question):
        """
        根据用户问题预测标签。
        """
        if self.model is None:
            print("模型未加载默认返回concept_explanation")
            return "concept_explanation"

        prediction=self.model.predict([question])
        label=prediction[0]
        return label

if __name__ == "__main__":
    router=MLRouter()
    test_questions = [
            "什么是 SQL 注入？",
            "根据资料解释 HTTPS 的工作流程",
            "Web 安全怎么学？",
            "最近有哪些高危漏洞？",
            "我想学习密码学应该怎么开始？",
            "结合知识库说明 XSS 的危害"
    ]

    for question in test_questions:
        label = router.route(question)
        print(question, "=>", label)