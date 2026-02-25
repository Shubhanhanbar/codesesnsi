import google.generativeai as genai
api_key="AIzaSyDH4uudGJoK4bqLGSywY4wHH8vCUGtk0-w"


MODEL = "gemini-3-flash-preview"
SYSTEM_PROMPT = """
Task:Generate an ATS-friendly resume.

Input:
Dish name

Output:
Step-by-step cooking instructions
Format:
Step 1: …
Step 2: …
Step 3: …

Instructions:
Search for the most popular and widely used cooking methods.
Provide clear, simple, and easy-to-follow steps.
Ensure the recipe matches the given ingredients.
If some ingredients are missing, suggest optional alternatives.
"""

def setup():
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=SYSTEM_PROMPT
    )

    chat = model.start_chat(history=[])
    return chat


def ask_ai_stream(chat, message: str) -> str:
    response = chat.send_message(message, stream=True)

    full_reply = ""

    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_reply += chunk.text   # ✅ fixed here

    print("\n")
    return full_reply


# Start Chat
chat = setup()

print("Chatbot started (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye 👋")
        break

    print("Bot: ", end="")
    ask_ai_stream(chat, user_input)