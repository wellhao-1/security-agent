# Day 20 日志



今天完成了 Security Learning Assistant Agent 的多模块分发整合。

主要完成内容包括：

- 创建 `src/llm.py`
- 将 `SimpleLLM` 从 `rag.py` 中抽离出来
- 修改 `src/rag.py`，统一从 `llm.py` 导入 `SimpleLLM`
- 实现规则版 Router：`RuleRouter`
- 明确四大路由标签：
  - `concept_explanation`
  - `rag_qa`
  - `study_advice`
  - `web_search`


concept_explanation  → 概念解释模块
rag_qa               → RAG 知识库问答模块
study_advice         → 学习建议模块
web_search           → 联网搜索模块