
import syntaxmatrix as smx
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KKEY")
llm = OpenAI(api_key=OPENAI_API_KEY)

PROFILE = os.getenv('PROFILE')

retrieved_chunks = [
"""The Enhanced Corrective Retrieval Augmented Generation (ECRAG) framework is introduced as an innovative approach to enhance the accuracy, relevance, and efficiency of information retrieval and response generation in knowledge augmented language models. Building upon existing systems like Retrieval Augmented""",

"""The rapid advancement of Artificial Intelligence (AI), particularly in Natural Language Processing (NLP), has led to the widespread adoption of Large Language Models (LLMs) for tasks like content generation, summarisation, and automated question answering. Despite their capabilities, LLMs often produce responses lacking factual grounding""",

"""Knowledge detection mechanisms help identify whether a query can be answered using internal domain knowledge or requires external augmentation. Traditional approaches rely on LLM confidence scores or simple keyword matching, but these methods are prone to false positives and negatives. Recent research combines lexical (e.g., BM25) and semantic (e.g., cosine similarity)"""
]

smx.enable_theme_toggle()
smx.set_widget_position("bottom")
smx.set_project_title("👀Syntax UI")
smx.set_theme("light")     
smx.set_ui_mode("bubble") 

# Register sidebar widgets.
smx.sidebar_text_input("sidebar_input", "Sidebar Input:", placeholder="Type here...")
smx.sidebar_button("sidebar_btn", "Do Sidebar Action", callback=lambda: smx.write("Sidebar action executed."))

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
        response = llm.chat.completions.create(
            model="gpt-4o-mini",
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

smx.text_input("user_query", "Enter query:", placeholder="Type here...")
smx.button("submit_query", "Submit", callback=create_conversation) 
smx.button("clear_chat", "Clear Chat", callback=clear_chat)

if __name__ == "__main__":
    smx.run()