import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="CareerFlow AI", page_icon="🚀", layout="centered")

# 2. Custom CSS for Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stActionButton {
        visibility: hidden;
    }
    /* Custom Header Gradient */
    .header-text {
        font-weight: 800;
        font-size: 2.5rem;
        background: -webkit-linear-gradient(#00d4ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Branding & Input
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.divider()
    st.markdown("### About")
    st.info("CareerFlow AI uses GPT-4o to provide strategic career coaching, resume feedback, and interview prep.")

# 4. App Header
st.markdown('<p class="header-text">CareerFlow AI</p>', unsafe_allow_html=True)
st.markdown("*Elevate your professional journey with AI-driven mentorship.*")
st.divider()

# 5. Chat Logic
if api_key:
    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are CareerFlow AI, a sophisticated executive mentor. Use bullet points for clarity, maintain a supportive yet direct tone, and always provide 'Next Steps' for the user."}
        ]

    # Display Chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input Field
    if prompt := st.chat_input("How can I help you grow today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("👈 Please enter your OpenAI API Key in the sidebar to begin your session.")
