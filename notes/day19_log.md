# Day 19 日志

## 今天完成

- 实现 src/rag.py
- 完成第一版 RAG Pipeline
- 将 Retriever 检索结果拼接进 Prompt
- 使用 SimpleLLM 模拟生成回答
- 成功完成“问题 → 检索 → Prompt → 回答”的流程


## 今天实现的流程

用户问题

↓

TfidfRetriever 检索 top-k chunks

↓

build_rag_prompt() 拼接 Prompt

↓

SimpleLLM.generate() 生成回答

↓

输出最终结果

---

## 明天计划

- 实现 concept_explanation 模块
- 实现 study_advice 模块
- 开始把不同标签接入不同处理流程