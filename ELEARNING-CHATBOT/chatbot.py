import streamlit as st
import time
import google.generativeai as genai
api_key="AIzaSyDH4uudGJoK4bqLGSywY4wHH8vCUGtk0-w"

MODEL="gemini-3-flash-preview"

SYSTEM_PROMPT=SYSTEM_PROMPT = SYSTEM_PROMPT = """
Task:Build a chatbot that provides cooking recipes.

Input:
Dish name

Output:
Step-by-step cooking instructions
Format:
Step 1:
Step 2:
Step 3:
......
Step N:
Instructions:
Search for the most popular and widely used cooking methods.
Provide clear, simple, and easy-to-follow steps.
Ensure the recipe matches the given ingredients.
If some ingredients are missing, suggest optional alternatives.
"""
def setup():
    genai.configure(api_key=api_key)
    model=genai.GenerativeModel(model_name=MODEL,
    system_instruction=SYSTEM_PROMPT)
    chat = model.start_chat(history=[])

    return chat

def ask_ai_stream(chat,message:str)->str:
    response=chat.send_message(message,stream=True)
    full_reply=""
    for chunk in response:
        print(chunk.text,end="",flush=True)
        full_reply+=chunk.text
    print("\n")
    return full_reply

chat=setup()


#page configuration
st.set_page_config(
    page_title="First Chatbot",
    page_icon=":)",
    layout="centered"
)

st.session_state.messages = []
st.session_state.bot_name = "LetHimCook"

with st.sidebar:
    st.title("Chatbot Settings")
    st.session_state.bot_name = st.text_input(
        "Bot Name",value=st.session_state.bot_name
    )

st.header("What you want to eat today?")
st.divider()



user_input = st.text_input("Enter Dish Name")
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": time.strftime("%H:%M:%S")
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Typing...."):
            time.sleep(0.8)
        response = ask_ai_stream(chat,user_input)
        st.markdown(response)
        
    st.session_state.messages.append({
        "role": "assitant",
        "content": "hello",
        "timestamp": time.strftime("%H:%M:%S")
    })