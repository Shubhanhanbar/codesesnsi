import streamlit as st
import time
import ollama
import json

SYSTEM_PROMPT="""
Tell me a story 
Instrucions:
1.keep story funny
2.keep story not more than 2 paragraph
3.like textbook format"""
#converstion list
chat_convo = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def ask_ai_stream(message: str) -> str:
    response = ollama.chat(
        model="phi3:mini",
        messages=chat_convo,
        options={"system": SYSTEM_PROMPT}
    )

    print(json.dumps(response, indent=4,default=str))
    return response['message']['content']


st.header("GEMUNI")

#page configuration
st.set_page_config(
    page_title="First Chatbot",
    page_icon=":)",
    layout="centered"
)

st.session_state.messages = []
st.session_state.bot_name = "Jarvis"

with st.sidebar:
    st.title("Chatbot Settings")
    st.session_state.bot_name = st.text_input(
        "Bot Name",value=st.session_state.bot_name
    )

st.header("Welcome to my First Chatbot")
st.divider()



user_input = st.text_input("Your prompt to chatbot")
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": time.strftime("%H:%M:%S")
    })
    chat_convo.append({
        "role": "user",
        "content": user_input,
        "timestamp": time.strftime("%H:%M:%S")
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Typing...."):
            time.sleep(0.8)
        response = ask_ai_stream(user_input)
        st.markdown(response)
        
    st.session_state.messages.append({
        "role": "assitant",
        "content": "hello",
        "timestamp": time.strftime("%H:%M:%S")
    })