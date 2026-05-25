# Day 22 日志

## 今天完成

- 实现 `src/train_router.py`
- 实现 `src/router_model.py`
- 使用 `data/router_dataset.json` 训练 Router 分类器
- 使用 TF-IDF 提取用户问题文本特征
- 使用 LinearSVC 训练四分类模型
- 生成 `models/router_model.pkl`
- 在 `app.py` 中接入机器学习版 Router


## 运行结果：

D:\Anaconda\python.exe C:\Users\11301\Desktop\security-agent\src\train_router.py 

============================================================
Router Dataset 统计
============================================================

样本数量: 122

各类别数量
-rag_qa: 18
-study_advice: 30
-web_search: 30
-concept_explanation: 44

============================================================
评估 Router 模型
============================================================

测试机准确率：1.000000

分类报告
                     precision    recall  f1-score   support

concept_explanation       1.00      1.00      1.00         9
             rag_qa       1.00      1.00      1.00         4
       study_advice       1.00      1.00      1.00         6
         web_search       1.00      1.00      1.00         6

           accuracy                           1.00        25
          macro avg       1.00      1.00      1.00        25
       weighted avg       1.00      1.00      1.00        25


模型保存成功：C:\Users\11301\Desktop\security-agent\models\router_model.pkl

D:\Anaconda\python.exe C:\Users\11301\Desktop\security-agent\src\router_model.py 
模型加载成功：C:\Users\11301\Desktop\security-agent\models/router_model.pkl
什么是 SQL 注入？ => concept_explanation
根据资料解释 HTTPS 的工作流程 => rag_qa
Web 安全怎么学？ => study_advice
最近有哪些高危漏洞？ => web_search
我想学习密码学应该怎么开始？ => study_advice
结合知识库说明 XSS 的危害 => rag_qa

