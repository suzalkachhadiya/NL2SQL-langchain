import streamlit as st
import google.generativeai as genai
from src.core.nl2sql_chain import NL2SQLChain

def initialize_session_state():
    """Initialize session state variables"""
    if "gemini_model" not in st.session_state:
        st.session_state["gemini_model"] = "models/gemini-1.5-flash"
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display the chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    st.title("Langchain NL2SQL Chatbot (Gemini Version)")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat history
    display_chat_history()
    
    # Handle user input
    if prompt := st.chat_input("What would you like to know about the database?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.spinner("Generating response..."):
            try:
                # Create NL2SQL chain
                chain = NL2SQLChain()
                
                # Get response
                response = chain.process_question(prompt, st.session_state.messages)
                
                # Display response
                with st.chat_message("assistant"):
                    st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 