# Security Agent

一个面向信息安全学习场景的轻量级 Agent 系统。

本项目结合了大语言模型、RAG 检索增强生成、Router 问题分发、Memory 对话记忆、用户问题改写和联网搜索能力，用于辅助学习 SQL 注入、XSS、CSRF、HTTPS、密码学、网络安全等信息安全基础知识。

---

## 项目功能

本项目目前支持以下功能：

- 安全概念解释
- 基于本地知识库的 RAG 问答
- 信息安全学习建议
- Tavily 联网搜索
- 智谱 GLM 大语言模型调用
- Router 问题分类
- 机器学习版 Router
- 多轮对话 Memory
- 用户问题改写
- Streamlit Web 界面

---

## 系统架构

整体流程如下：

```text
用户问题
    ↓
Memory 读取历史对话
    ↓
问题改写
    ↓
Router 分类
    ↓
分发到不同模块
    ├── concept_explanation → 概念解释
    ├── rag_qa              → RAG 知识库问答
    ├── study_advice        → 学习建议
    └── web_search          → 联网搜索
    ↓
LLM 生成回答
    ↓
Memory 保存对话
    ↓
返回结果
```

---

## 项目结构

```text
security-agent/
│
├── data/
│   ├── *.txt
│   └── router_dataset.json
│
├── processed_data/
│   └── chunks.json
│
├── models/
│   └── router_model.pkl
│
├── src/
│   ├── load_docs.py
│   ├── chunk_docs.py
│   ├── retriever.py
│   ├── rag.py
│   ├── llm.py
│   ├── router.py
│   ├── router_model.py
│   ├── train_router.py
│   ├── concept.py
│   ├── advisor.py
│   ├── web_search.py
│   ├── memory.py
│   └── utils.py
│
├── app.py
├── web_app.py
├── test_agent.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 核心模块说明

### 1. 本地知识库

`data/` 目录中保存信息安全相关知识文本，例如：

- SQL 注入
- XSS
- CSRF
- HTTPS
- 哈希函数
- 对称加密
- 非对称加密
- 数字签名
- 防火墙
- IDS / IPS

这些文本作为 RAG 的本地知识来源。

---

### 2. 文档读取与切块

`src/load_docs.py` 用于读取 `data/` 下的知识库文件。

`src/chunk_docs.py` 用于将长文本切分为较小的 chunk，并保存到：

```text
processed_data/chunks.json
```

---

### 3. Retriever 检索器

`src/retriever.py` 实现了基于 TF-IDF 的文本检索器。

流程如下：

```text
用户问题
    ↓
TF-IDF 向量化
    ↓
计算相似度
    ↓
返回 Top-k 相关文本块
```

---

### 4. RAG 问答模块

`src/rag.py` 实现 RAG 问答流程。

流程如下：

```text
用户问题
    ↓
Retriever 检索相关资料
    ↓
构建 Prompt
    ↓
调用 LLM
    ↓
生成回答
```

---

### 5. Router 问题分发

项目实现了两种 Router。

`src/router.py` 是规则版 Router，通过关键词判断问题类型。

`src/router_model.py` 是机器学习版 Router，使用 TF-IDF + SVM 对用户问题进行分类。

支持四类标签：

```text
concept_explanation
rag_qa
study_advice
web_search
```

---

### 6. LLM 模块

`src/llm.py` 接入智谱 GLM API，用于生成真实模型回答。

---

### 7. 联网搜索模块

`src/web_search.py` 接入 Tavily Search API，用于获取实时联网搜索结果，并调用 LLM 对搜索结果进行总结。

---

### 8. Memory 与问题改写

`src/memory.py` 实现简单对话记忆。

系统可以保存最近几轮对话，并在多轮问答中进行问题改写。

例如：

```text
用户：什么是 SQL 注入？
用户：那怎么防御？
```

系统会尝试改写为：

```text
SQL 注入怎么防御？
```

---

### 9. Web 界面

`web_app.py` 使用 Streamlit 构建 Web 演示界面。

支持：

- 输入问题
- 显示 Agent 回答
- 显示 Router 标签
- 显示原始问题
- 显示改写问题
- 查看 Prompt
- 查看 RAG 检索结果
- 查看 Tavily 搜索结果
- 查看和清空 Memory

---

## 安装依赖

```bash
pip install -r requirements.txt
```

---

## 环境变量配置

请在项目根目录创建 `.env` 文件。

```env
ZHIPU_API_KEY=your_zhipu_api_key
ZHIPU_MODEL=glm-5.1
ZHIPU_API_BASE=https://open.bigmodel.cn/api/paas/v4

TAVILY_API_KEY=your_tavily_api_key
```


## 运行方式

### 1. 生成知识库 chunks

python src/chunk_docs.py
生成：
processed_data/chunks.json


### 2. 训练机器学习 Router


python src/train_router.py
生成：
models/router_model.pkl


### 3. 命令行运行 Agent

python app.py

### 4. 启动 Web 界面


streamlit run web_app.py

浏览器打开后即可使用 Web Demo。



## 测试问题

可以使用以下问题进行测试：

```text
什么是 SQL 注入？
```

```text
根据资料解释 HTTPS 的工作流程
```

```text
Web 安全怎么学？
```

```text
最近有哪些高危漏洞？
```

```text
那怎么防御？
```

---

## 当前项目亮点

- 实现了完整的轻量级 Agent 工作流
- 支持 Router 多模块分发
- 支持本地知识库 RAG 问答
- 支持 TF-IDF Retriever
- 支持 TF-IDF + SVM 机器学习 Router
- 接入真实智谱 GLM API
- 接入真实 Tavily Search API
- 支持 Memory 和用户问题改写
- 提供 Streamlit Web 可视化界面
- 支持查看 Prompt、RAG 检索结果和搜索结果

---

## 当前限制

当前项目仍然是轻量级原型，存在以下限制：

- Retriever 使用 TF-IDF，语义检索能力有限
- 暂未接入向量数据库
- Memory 只是短期记忆（三轮对话），未实现长期记忆
- Router 分类效果依赖训练数据质量
- Web Search 结果依赖 Tavily API
- 尚未加入完整日志系统和异常监控

---

## 后续优化方向

后续可以继续优化：

- 使用 Embedding + 向量数据库替代 TF-IDF 检索
- 接入 ChromaDB、FAISS 或 Milvus
- 增加 RAG 评估机制
- 增强 Router 数据集
- 优化问题改写策略
- 增加日志系统
- 增加单元测试
- 使用 FastAPI 提供后端接口
- 将系统部署到云端

---

## 项目定位

本项目通过 Router 对用户问题进行分类，并根据问题类型调用不同工具或模块，实现概念解释、知识库问答、学习建议、联网搜索和多轮对话能力。
