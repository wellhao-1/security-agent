# Day 18 日志

## 今天完成

- 实现 src/retriever.py
- 读取 processed_data/chunks.json
- 使用 TF-IDF 构建 chunk 检索索引
- 使用 cosine similarity 计算用户问题和 chunk 的相似度
- 成功返回 top-k 相关文本块

---


## 今天实现的流程

processed_data/chunks.json

↓

TfidfVectorizer

↓

chunk_matrix

↓

用户问题向量

↓

cosine_similarity

↓

top-k chunks

---

## 明天计划

- 实现 rag.py
- 将 Retriever 检索结果拼接成 Prompt
- 完成第一版 RAG 问答流程