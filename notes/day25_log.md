# Day 25 日志

## 今天完成

- 新增 `web_app.py`
- 使用 Streamlit 搭建 Web 界面
- 将原来的命令行 Agent 包装成浏览器可交互页面
- 支持用户在网页中输入问题
- 支持显示 Agent 回答
- 支持保留聊天记录
- 支持显示 Router 标签
- 支持显示原始问题
- 支持显示改写后的问题
- 支持查看模块 `detail`
- 支持查看最终 Prompt
- 支持查看 RAG 检索结果
- 支持查看 Tavily 搜索结果
- 支持查看 Memory
- 支持清空 Memory
- 支持重新初始化 Agent

---

## 

Streamlit 的核心机制是：

```text
每次用户交互
    ↓
整个 Python 脚本重新运行
    ↓
通过 st.session_state 保留关键状态
    ↓
重新渲染页面