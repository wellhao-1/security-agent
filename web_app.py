import streamlit as st

from app import SecurityAgent


st.set_page_config(
    page_title="Security Learning Assistant Agent",
    page_icon="🛡️",
    layout="wide"
)


def init_agent():
    """
    初始化 SecurityAgent。

    注意：
    Streamlit 每次交互都会重新运行脚本，
    所以必须把 agent 放进 session_state，
    避免每次都重新构建 RAG 索引。
    """

    agent = SecurityAgent()

    agent.build()

    return agent


def ensure_session_state():
    """
    初始化 Streamlit 会话状态。
    """

    if "agent" not in st.session_state:
        with st.spinner("正在初始化 Security Agent，请稍等..."):
            st.session_state.agent = init_agent()

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "last_result" not in st.session_state:
        st.session_state.last_result = None


def render_sidebar():
    """
    渲染侧边栏。
    """

    st.sidebar.title("Security Agent")

    st.sidebar.markdown(
        """
        当前系统能力：

        - 真实智谱 LLM
        - Tavily 联网搜索
        - 本地知识库 RAG
        - MLRouter / RuleRouter
        - 对话 Memory
        - 用户问题改写
        """
    )

    st.sidebar.divider()

    st.sidebar.subheader("快捷操作")

    if st.sidebar.button("查看 Memory"):
        memory_text = st.session_state.agent.memory.get_context()

        if memory_text == "":
            st.sidebar.info("当前没有对话记忆。")
        else:
            st.sidebar.text_area(
                "当前 Memory",
                memory_text,
                height=300
            )

    if st.sidebar.button("清空 Memory"):
        st.session_state.agent.memory.clear()
        st.session_state.chat_messages = []
        st.session_state.last_result = None
        st.sidebar.success("Memory 已清空。")

    if st.sidebar.button("重新初始化 Agent"):
        with st.spinner("正在重新初始化 Agent..."):
            st.session_state.agent = init_agent()
            st.session_state.chat_messages = []
            st.session_state.last_result = None
        st.sidebar.success("Agent 已重新初始化。")

    st.sidebar.divider()

    st.sidebar.subheader("测试问题")

    examples = [
        "什么是 SQL 注入？",
        "根据资料解释 HTTPS 的工作流程",
        "Web 安全怎么学？",
        "最近有哪些高危漏洞？",
        "那怎么防御？"
    ]

    for example in examples:
        st.sidebar.code(example)


def render_header():
    """
    渲染页面标题。
    """

    st.title("🛡️ Security Learning Assistant Agent")

    st.markdown(
        """
        一个面向信息安全学习场景的轻量级 Agent 系统。

        支持：

        `概念解释` · `RAG 知识库问答` · `学习建议` · `联网搜索` · `Memory` · `问题改写`
        """
    )

    st.divider()


def render_chat_history():
    """
    渲染聊天记录。
    """

    for message in st.session_state.chat_messages:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            st.markdown(content)


def render_debug_panel():
    """
    渲染调试信息面板。
    """

    result = st.session_state.last_result

    if result is None:
        return

    st.divider()

    st.subheader("🔍 调试信息")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Router 标签**")
        st.code(result.get("label", ""))

    with col2:
        st.markdown("**原始问题**")
        st.code(result.get("question", ""))

    rewritten_question = result.get("rewritten_question", result.get("question", ""))

    if rewritten_question != result.get("question", ""):
        st.markdown("**改写后的问题**")
        st.code(rewritten_question)

    detail = result.get("detail", {})

    with st.expander("查看模块 detail"):
        st.json(detail)

    if isinstance(detail, dict):
        if "prompt" in detail and detail["prompt"]:
            with st.expander("查看最终 Prompt"):
                st.text(detail["prompt"])

        if "retrieved_chunks" in detail:
            with st.expander("查看 RAG 检索结果"):
                for idx, chunk in enumerate(detail["retrieved_chunks"]):
                    st.markdown(f"### Chunk {idx + 1}")
                    st.write(f"来源文件：`{chunk.get('filename', '')}`")
                    st.write(f"相似度：`{chunk.get('score', 0):.4f}`")
                    st.text(chunk.get("content", "")[:1000])

        if "search_results" in detail:
            with st.expander("查看 Tavily 搜索结果"):
                for idx, item in enumerate(detail["search_results"]):
                    st.markdown(f"### 搜索结果 {idx + 1}")
                    st.write(f"标题：{item.get('title', '')}")
                    st.write(f"链接：{item.get('url', '')}")
                    st.write(f"摘要：{item.get('snippet', '')}")
                    st.write(f"相关性分数：{item.get('score', '')}")


def handle_user_input():
    """
    处理用户输入。
    """

    user_input = st.chat_input("请输入你的问题...")

    if not user_input:
        return

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Agent 正在思考..."):
            result = st.session_state.agent.answer(user_input)

            answer = result.get("answer", "")

            st.markdown(answer)

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.session_state.last_result = result


def main():
    """
    Streamlit Web App 主入口。
    """

    ensure_session_state()

    render_sidebar()

    render_header()

    render_chat_history()

    handle_user_input()

    render_debug_panel()


if __name__ == "__main__":
    main()