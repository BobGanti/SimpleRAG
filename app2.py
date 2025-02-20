
import syntaxmatrix as smx
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set API key.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
XAI_API_KEY = os.getenv('XAI_API_KEY')

LLMs = [
    OpenAI(api_key=OPENAI_API_KEY),
    OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"),
    OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1"),
]

MODELs = [
    "gpt-4o-mini", 
    'deepseek-chat', 
    'grok-2-latest',
]

PROFILE = os.getenv('PROFILE')

retrieved_chunks = [
"""The Enhanced Corrective Retrieval Augmented Generation (ECRAG) framework is introduced as an innovative approach to enhance the accuracy, relevance, and efficiency of information retrieval and response generation in knowledge augmented language models. Building upon existing systems like Retrieval Augmented""",

"""The rapid advancement of Artificial Intelligence (AI), particularly in Natural Language Processing (NLP), has led to the widespread adoption of Large Language Models (LLMs) for tasks like content generation, summarisation, and automated question answering. Despite their capabilities, LLMs often produce responses lacking factual grounding""",

"""Knowledge detection mechanisms help identify whether a query can be answered using internal domain knowledge or requires external augmentation. Traditional approaches rely on LLM confidence scores or simple keyword matching, but these methods are prone to false positives and negatives. Recent research combines lexical (e.g., BM25) and semantic (e.g., cosine similarity)"""
]

# Setup 
# smx.set_ui_mode("default") or "bubble", "card"
smx.set_project_title(f"👀SMX UI")    
smx.enable_theme_toggle()
# smx.set_theme("dark")   or "default"


def process_query(query, history, chunks): 
    prompt =[
        {
            "role": "system",
            "content": PROFILE
        },
        {
            "role": "user",
            "content": "Generate a response to the given query, limiting your knowledge " "to the given content. Also refer to the chat history if needed."
        },
        {
            "role": "assistant",
            "content": f"Query: {query}\n\nContext: {chunks}\n\nHistory: {history}\n\n"
        }
    ]

    try:
        response = LLMs[2].chat.completions.create(
            model=MODELs[2],
            messages=prompt,
            temperature=0.3,
            max_tokens=300
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error: {str(e)}"

    return answer 

def create_conversation():
    query = smx.get_text_input_value("user_query")
    chat_history = smx.get_chat_history()
    answer = process_query(query, chat_history, retrieved_chunks)
    chat_history.append(("👩🏿‍🦲", query))
    chat_history.append(("👀", answer))
    
    smx.set_chat_history(chat_history)
    smx.clear_text_input_value("user_query")

def clear_chat():
    smx.clear_chat_history()

smx.text_input("user_query", "Enter query:")
smx.button("submit_query", "Submit", callback=create_conversation) 
smx.button("clear_chat", "Clear Chat", callback=clear_chat)

if __name__ == "__main__":
    smx.run()