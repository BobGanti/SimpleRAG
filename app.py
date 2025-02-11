from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Set your OpenAI API key.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

LLMs = [
    OpenAI(api_key=OPENAI_API_KEY),
    OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
]

MODELs = [
    "gpt-4o-mini", 
    'deepseek-chat', 
]

PROFILE = os.getenv('PROFILE')

chat_history = []

def process_query(query, chat_history):
    
    # Build the conversation for the OpenAI API.
    prompt = [{"role": "system", "content": 
               "You are an AI assistant with expertise in generating meaningful responses to queries " "based on given context."}]
    
    for sender, message in chat_history:
        if sender == "User":
            prompt.append({"role": "user", "content": message})
        elif sender == "Bot":
            prompt.append({"role": "assistant", "content": message})
    prompt.append({"role": "user", "content": query})
    
    try:
        response = LLMs[0].chat.completions.create(
            model=MODELs[0], 
            messages=prompt,
            temperature=0.7,
            max_tokens=150
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error: {str(e)}"
    print("Bot:", answer)
    print()

def create_conversation():
    query = input("What is your query: ")
    print()
    while query != 'no':
        process_query(query, chat_history)
        query = input("You: ")
        print()

create_conversation()
