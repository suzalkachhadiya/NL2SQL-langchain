import streamlit as st
import os
import google.generativeai as genai
from utils import invoke_chain  # Assuming this handles NL2SQL conversion
from dotenv import load_dotenv

load_dotenv()
st.title("Langchain NL2SQL Chatbot (Gemini Version)")

# Set Gemini API key from Streamlit secrets
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set a default model
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "models/gemini-1.5-flash"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Generating response..."):
        # Create model instance
        model = genai.GenerativeModel(st.session_state["gemini_model"])
        chat = model.start_chat(history=[
            {"role": msg["role"], "parts": [msg["content"]]} for msg in st.session_state.messages
        ])
        gemini_response = chat.send_message(prompt)

        # You can plug in your `invoke_chain` logic here if needed
        response_text = invoke_chain(prompt,st.session_state.messages)

        with st.chat_message("assistant"):
            st.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})
