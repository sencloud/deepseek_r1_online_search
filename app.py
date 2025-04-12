import streamlit as st
import asyncio
from deepseek_client import DeepSeekClient
import time

# 页面配置
st.set_page_config(
    page_title="DeepSeek R1 联网搜索",
    page_icon="🔍",
    layout="wide"
)

# CSS样式
st.markdown("""
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
    flex-direction: column;
}
.user-message {
    background-color: #e6f3ff;
    border-left: 5px solid #2b6cb0;
}
.assistant-message {
    background-color: #f0f4f8;
    border-left: 5px solid #4a5568;
}
.message-content {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
}
.avatar {
    min-width: 30px;
    margin-right: 1rem;
    font-size: 1.5rem;
}
.message-text {
    flex-grow: 1;
}
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# 标题
st.title("DeepSeek R1 联网搜索")

st.markdown("---")
st.markdown("基于Streamlit + Python实现，支持多轮对话与流式输出，不显示思考过程，故响应时间相对较长") 

# 对话历史显示
for idx, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        with st.container():
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-content">
                    <div class="avatar">👤</div>
                    <div class="message-text">{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-content">
                    <div class="avatar">🤖</div>
                    <div class="message-text">{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# 输入框
with st.form(key="search_form", clear_on_submit=True):
    user_input = st.text_area("输入您的问题:", height=100, key="user_input")
    submit_button = st.form_submit_button("发送")

# 处理用户输入
if submit_button and user_input:
    # 将用户消息添加到历史
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.conversation_started = True
    
    # 创建临时的信息占位
    message_placeholder = st.empty()
    message_placeholder.markdown("""
    <div class="chat-message assistant-message">
        <div class="message-content">
            <div class="avatar">🤖</div>
            <div class="message-text">思考中...</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 准备调用DeepSeek API
    full_response = ""
    
    # 创建DeepSeek客户端
    client = DeepSeekClient()
    
    # 准备消息
    formatted_messages = [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in st.session_state.messages
    ]
    
    # 使用asyncio调用API并流式输出结果
    async def get_streaming_response(response_text):
        # 调用DeepSeek API
        response = await client.chat_completion(
            messages=formatted_messages,
            stream=True
        )
        
        # 流式处理响应
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                response_text += content
                
                # 更新UI
                message_placeholder.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="message-content">
                        <div class="avatar">🤖</div>
                        <div class="message-text">{response_text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 短暂等待以模拟打字效果
                time.sleep(0.01)
        
        return response_text
    
    # 运行异步函数
    full_response = asyncio.run(get_streaming_response(full_response))
    
    # 保存完整的助手响应到对话历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # 使用JavaScript强制页面滚动到底部
    st.markdown("""
    <script>
        function scrollToBottom() {
            window.scrollTo(0, document.body.scrollHeight);
        }
        scrollToBottom();
    </script>
    """, unsafe_allow_html=True)