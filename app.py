import syntaxmatrix as smx
from syntaxmatrix.plottings import figure, plotly
import os
from openai import OpenAI
from dotenv import load_dotenv
from syntaxmatrix.file_processor import recursive_text_split
from io import BytesIO
from PyPDF2 import PdfReader

load_dotenv(override=False, verbose=False)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROFILE = os.getenv("PROFILE")

LLMs = [
    OpenAI(api_key=OPENAI_API_KEY),
    OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"),
    OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1"),
    OpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/"),
]
MODELs = {
    "gpt":["gpt-4o-mini"], 
    "deepseek":["deepseek-chat"], 
    "grok":["grok-2-latest", "grok-3"],
    "gemini":["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-pro"]
}

llm = LLMs[3]
model = MODELs["gemini"][0]

smx.set_ui_mode("bubble")
# smx.set_site_icon("𓃑")
# smx.set_site_logo("ABC")
# smx.set_project_title("ABC DATA")
# smx.set_site_title("ABC")

sys_chunks = smx.load_pdf_chunks()

def process_query(query, history, context): 
    INSTRUCTION = """Generate a response to the given query based on the given content. Use the chat history to stay in context. Refer to your training knowledge if content lacks sufficient knowledge to generate a response.
    """
    prompt = [
        {"role": "system", "content": PROFILE},
        {"role": "user", "content": INSTRUCTION},
        {"role": "assistant", "content": f"Query: {query}\n\nContext: {context}\n\nHistory: {history}\n\nAnswer: "}
    ]

    try:
        response = llm.chat.completions.create(
            model=model,
            messages=prompt,
            temperature=0.3,
            max_tokens=500
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error: {str(e)}"
    return answer 

def create_conversation():
    chat_history = smx.get_chat_history()
    sid = smx.get_session_id()

    # Get any user-uploaded files and process them
    personal_chunks = smx.get_user_chunks(sid) or []
    context = list(sys_chunks.values())
    if personal_chunks:
        [context.append(p_ch) for p_ch in personal_chunks]

    query = smx.get_text_input_value("user_query").strip()
    if not query:
        smx.warning("Enter a query.")
        return

    trimmed_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
    answer = process_query(query, trimmed_history, context)

    chat_history.append(("User", query))
    chat_history.append(("Bot", answer))

    smx.set_chat_history(chat_history)
    smx.clear_text_input_value("user_query")
  
def analysis():  
   
    return

analysis()

def clear_chat():
    smx.clear_chat_history()

# Activate System Widgets
smx.text_input("user_query", "Enter query:", placeholder="Type your query here...")
smx.button("submit_query", "Submit", callback=create_conversation) 
smx.file_uploader("user_pdfs", "Upload PDF files:", accept_multiple_files=True)

# Register Custom Widgets
smx.button("clear_chat", "Clear Chat", callback=clear_chat)
smx.button("analysis", "Analyse", callback=analysis)

if __name__ == "__main__":
    smx.run()
