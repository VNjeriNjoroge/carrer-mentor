import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Career Mentor", page_icon="💼")

st.title("💼 AI Career Mentor")
st.caption("Strategic guidance for your professional journey.")

# Securely input OpenAI API Key
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are an expert Career Mentor with 20+ years of experience in executive coaching and HR. Your tone is encouraging, professional, and highly strategic. Focus on actionable advice, resume optimization, and interview preparation."}
        ]

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask about your career..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.info("Please add your OpenAI API key in the sidebar to continue.", icon="🔑")
