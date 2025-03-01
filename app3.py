
import syntaxmatrix as smx
import os
from openai import OpenAI
from dotenv import load_dotenv

retrieved_chunks = [
    """Retrieval-Augmented Generation (RAG) systems combine information retrieval with language 
    model generation to enhance factual accuracy in outputs. The framework retrieves relevant 
    context from a document corpus and integrates this context into the generative process. Lewis 
    et al. (2020) demonstrated that RAG systems reduce hallucinations and improve response 
    quality by grounding the generation process in actual documents. However, the retrieval 
    component in standard RAG systems struggles with speed and scalability as the size of the 
    corpus increases.""",
    
    """Corrective Retrieval Augmented Generation (CRAG) introduces a corrective re-ranking 
    mechanism that evaluates retrieved passages for relevance before feeding them to the 
    generative model. This additional step improves grounding and coherence in responses. 
    However, CRAG inherits certain limitations from RAG, particularly in handling ambiguous 
    queries and ensuring high retrieval accuracy when processing large or unstructured datasets. 
    """,

    """The Enhanced Corrective Retrieval Augmented Generation (ECRAG) framework is introduced as an innovative approach to enhance the accuracy, relevance, and efficiency of information retrieval and response generation in knowledge augmented language models. Building upon existing systems like Retrieval Augmented""",
    
    """Knowledge detection mechanisms help identify whether a query can be answered using internal domain knowledge or requires external augmentation. Traditional approaches rely on LLM confidence scores or simple keyword matching, but these methods are prone to false positives and negatives. Recent research combines lexical (e.g., BM25) and semantic (e.g., cosine similarity)""",
]

load_dotenv()

# APIs Setup.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
XAI_API_KEY = os.getenv('XAI_API_KEY')

PROFILE = os.getenv('PROFILE')

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

llm = LLMs[0]
model = MODELs[0]

# # Project Settings 
custom_theme = {
    "background": "#ffffff",
    "text_color": "#000000",
    "nav_background": "#123456",
    "nav_text": "#ffffff",
    "chat_background": "#f7f7f7",
    "chat_border": "#cccccc",
    "widget_background": "#dddddd",
    "widget_border": "#123456",
    "sidebar_background": "#eeeeee",
    "sidebar_text": "#333333"
}
smx.set_theme("my", custom_theme)

smx.set_site_title("smx")
smx.set_site_logo("SMX")
smx.set_user_icon("👩🏿‍🦲")
smx.set_bot_icon("👀")
smx.set_site_icon("𓃑")
smx.set_project_title("SMX UI")    
smx.enable_theme_toggle()
smx.set_ui_mode("default")

def process_query(query, history, chunks=""): 
    INSTRUCTION = "Generate a response to the given query, limiting your knowledge " "to the given content. Also refer to the chat history if needed."
    prompt =[
        {"role": "system", "content": PROFILE},
        {"role": "user", "content": INSTRUCTION},
        {"role": "assistant", "content": f"Query: {query}\n\nContext: {chunks}\n\nHistory: {history}\n\n"}
    ]

    try:
        response = llm.chat.completions.create(
            model=model,
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
    
    chat_history.append(("User", query))
    chat_history.append(("Bot", answer))
    smx.set_chat_history(chat_history)

    smx.clear_text_input_value("user_query")

def clear_chat():
    smx.clear_chat_history()

smx.text_input("user_query", "Enter query:")
smx.button("submit_query", "Submit", callback=create_conversation) 
smx.button("clear_chat", "Clear Chat", callback=clear_chat)

if __name__ == "__main__":
    smx.run()