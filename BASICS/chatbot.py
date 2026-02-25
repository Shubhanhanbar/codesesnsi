#import required tools
import ollama

#define your SYSTEM Prompt
SYSTEM_PROMPT = """
Tell me a story
Instructions:
1. Keep story funny
2. Keep the story not more than 2 paragraphs
"""

# Conversation list (start with system prompt)
chat_convo = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# conversation loop
def chat_with_ollama():
    print("Welcome to storyline (type 'exit' to quit)\n")

    while True:
        try:
            user_input = input("User: ").strip()
            
            if user_input.lower() == "exit":
                print("User quit")
                break

        except KeyboardInterrupt:
            print("\nUser quit")
            break

        # Append user input correctly
        chat_convo.append({
            "role": "user",
            "content": user_input
        })

        try:
            print("Chatbot prompt started...\n")

            response = ollama.chat(
                model="phi3:mini",
                messages=chat_convo
            )

            # Extract assistant response text
            bot_reply = response["message"]["content"]

            # Append assistant reply
            chat_convo.append({
                "role": "assistant",
                "content": bot_reply
            })

            print("Bot:", bot_reply, "\n")

        except Exception as e:
            print("Error:", e)

# Run function
chat_with_ollama()