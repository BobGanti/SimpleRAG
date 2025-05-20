# SyntaxMatrix AI Framework v1.3.1

**SyntaxMatrix:** A customizable framework for Python AI assistant projects.

---
**DEMO:**
<a href="https://www.youtube.com/watch?v=PtGH1kaWm9M" target="_blank">
  <img src="https://img.youtube.com/vi/PtGH1kaWm9M/0.jpg" width="400">
</a>

<table>
  <tr>
    <td>
      <a href="https://www.youtube.com/watch?v=PtGH1kaWm9M" target="_blank">
        <img src="https://img.youtube.com/vi/PtGH1kaWm9M/0.jpg" width="270">
      </a>
      <p align="center"><strong>Demo Video</strong></p>
    </td>
    <td>
      <a href="https://www.youtube.com/watch?v=6CS5_ScJdrw" target="_blank">
        <img src="https://img.youtube.com/vi/6CS5_ScJdrw/0.jpg" width="270">
      </a>
      <p align="center"><strong>Tutorial Video</strong></p>
    </td>
  </tr>
</table>



---
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Overview

`syntaxmatrix` is a full-stack Python library that lets you build interactive chat-style front-ends for AI apps without diving into a full web framework. It provides:

- Rapid widget registration (text inputs, buttons, file uploaders)
- Dynamic theme toggling and multiple UI modes
- Built-in PDF ingestion & chunking
- Stylized feedback (success, error, warning, info)
- Admin panel, session management, and more

Ideal for Retrieval-Augmented Generation (RAG), data explorers, or any AI assistant interface.

---

## Quick Links

- `pip install syntaxmatrix`
---

## Features

- **Rapid UI Creation**: One-line calls to register `text_input`, `button`, `file_uploader`, etc.
- **Built-in Chat Loop**:
  - `user_query` (text input),
  - `submit_query` (send button),
  - `user_pdfs` (PDF uploader + chunking).
- **Custom Widgets**: Register any keys you like—just provide matching handler logic.
- **PDF Ingestion**: `load_pdf_chunks(directory)` Domain data that augments LLM's knowledge/ and returns a `{filename: [chunks,…]}` map.
- **Session File Uploads**: `get_user_chunks()`, for per-session user files.
- **Dynamic Themes**: `enable_theme_toggle()`, `set_theme()`, plus `list_themes()`.
- **Multiple UI Modes**: `set_ui_mode()` supports `default`, `bubble`, `card`, `smx` and `list_ui_modes()`.
- **Rich Output**: `markdown()`, `latex()`, `plt_plot()`, `plotly_plot()`, plus `error()`, `warning()`, `success()`, `info()`.
- **Branding Helpers**: `set_user_icon()`, `set_bot_icon()`, `set_site_icon()`, `set_site_logo()`, `set_site_title()`, `set_project_title()`.
- **Session Management**: Named chat sessions with rename/delete; session IDs via `get_session_id()`.

---

## Installation

```bash
pip install syntaxmatrix
```
or if upgrading

```bash
pip install --upgrade syntaxmatrix
```

## Quick-Start Snippet

This minimal example uses the **built-in** chat flow (no custom keys required):

```python
import syntaxmatrix as smx
from syntaxmatrix.plottings import figure, plotly
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv(override=False, verbose=False)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROFILE = os.getenv("PROFILE")

LLMs = {
    "gpt": OpenAI(api_key=OPENAI_API_KEY),
    "deepseek": OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"),
    "grok": OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1"),
    "gemini": OpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/"),
}
MODELs = {
    "gpt":["gpt-4o-mini"], 
    "deepseek":["deepseek-chat"], 
    "grok":["grok-2-latest"],
    "gemini":["gemini-2.0-flash-lite", "gemini-2.0-flash"]
}

llm = LLMs["gpt"]
model = MODELs["gpt"][0]

smx.set_ui_mode("bubble")  # [default, card, bubble, smx]
smx.set_theme("chark", "chark")
smx.set_project_title("RAG System") 
smx.set_site_logo("SMX")
smx.set_site_title("smx")
smx.set_user_icon("😸")
smx.set_bot_icon("💀")
smx.set_site_icon("👃")   
# smx.enable_theme_toggle()

sys_chunks = smx.load_sys_chunks()

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
    # Augment the Domain data wit the user data
    if personal_chunks:
        for p_ch in personal_chunks:
            context.append(p_ch)

    query = smx.get_text_input_value("user_query").strip()
    # Handle the "Enter" keyboard key if pressed when the text input is empty.
    if not query:  
        smx.warning("Enter a query.")
        return

    # Consider only the last n=10 chat cycles in the chat history
    trimmed_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
    answer = process_query(query, trimmed_history, context)

    chat_history.append(("User", query))
    chat_history.append(("Bot", answer))

    smx.set_chat_history(chat_history)
    smx.clear_text_input_value("user_query")

# Activate System Widgets
smx.text_input("user_query", "Enter query:", placeholder="Type your query here...")
smx.button("submit_query", "Submit", callback=create_conversation) 
smx.file_uploader("user_pdfs", "Upload PDF files:", accept_multiple_files=True)

# Register Custom Widgets
def clear_chat():
    smx.clear_chat_history()

smx.button("clear_chat", "Clear Chat", callback=clear_chat)


if __name__ == "__main__":
    smx.run()

```

> **Note:** If you register different keys, you must also adapt your handlers and/or the request-processing logic to match those names.

---

## Registering Custom Widgets

You’re not limited to the three defaults. Example:

```python
# Custom keys:
smx.text_input("query_box", "Your query…")
smx.button("ask_btn", "Ask", callback=my_ask_handler)
smx.file_uploader(
    "pdf_docs",
    "Attach Documents", 
    accept_multiple_files=True,
    callback=my_upload_handler
)
```

Then your `my_ask_handler()` must read from `smx.get_text_input_value("query_box")`, and you’ll need to implement or wrap the chat loop yourself if you deviate from the built-ins.

---

## API Reference

### App Lifecycle & Branding

| Function                                              | Description                                                                      |
| ----------------------------------------------------- | -------------------------------------------------------------------------------- |
| `run()`                                               | Launches the Flask server and opens a browser window                             |
| `set_site_title(title: str)`                          | Sets the navbar site title                                                       |
| `set_project_title(title: str)`                       | Sets the main project heading                                                    |
| `set_user_icon(icon: str)`                            | Emoji/text for user messages                                                     |
| `set_bot_icon(icon: str)`                             | Emoji/text for bot messages                                                      |
| `set_site_icon(icon: str)`                            | Small icon in the browser tab                                                    |
| `set_site_logo(logo: str)`                            | Text/logo in the navbar                                                          |

### Theming & Modes

| Function                                              | Description                                                                      |
| ----------------------------------------------------- | -------------------------------------------------------------------------------- |
| `enable_theme_toggle()`                               | Show a light/dark toggle link in the navbar                                      |
| `disable_theme_toggle()`                              | Hide the theme toggle                                                             |
| `set_theme(name: str, theme_dict?: dict)`             | Switch or define a custom theme                                                   |
| `list_themes() -> List[str]`                          | Get all available theme names                                                     |
| `set_ui_mode(mode: str)`                              | Choose layout: `default`, `bubble`, `card`, `smx`                                 |
| `list_ui_modes() -> Tuple[str,…]`                     | Available UI modes                                                                |

### Built-in Widgets & Flow

| Function                                              | Description                                                                      |
| ----------------------------------------------------- | -------------------------------------------------------------------------------- |
| `text_input(key, label, placeholder="")`             | Register a text box. For built-in chat use key=`user_query`.                      |
| `button(key, label, callback=None)`                   | Register a button. For built-in chat use key=`submit_query`.                      |
| `file_uploader(key, label, accept_multiple_files=False, callback=None)` | Register a file upload. For PDF chunking use key=`user_pdfs`.       |
| `get_text_input_value(key)`                           | Read current text in a box                                                        |
| `clear_text_input_value(key)`                         | Clear the text box                                                                |
| `get_file_upload_value(key)`                          | Access raw file objects uploaded                                                  |

### PDF & File-Chunk APIs

| Function                                              | Description                                                                      |
| ----------------------------------------------------- | -------------------------------------------------------------------------------- |
| `load_pdf_chunks(directory: str = "uploads/sys")`      | Ingest all system PDFs → split into chunks → cache → return `{file:[chunks]}`     |
| `get_session_id() -> str`                             | Current chat session UUID                                                          |
| `add_user_chunks(sess_id: str, chunks: List[str])`    | Store user-uploaded text chunks                                                   |
| `get_user_chunks(sess_id: str) -> List[str]`          | Retrieve stored user chunks                                                       |
| `clear_user_chunks(sess_id: str)`                     | Remove all user chunks for session                                                |

### Rich & Stylized Output

| Function                                              | Description                                                                      |
| ----------------------------------------------------- | -------------------------------------------------------------------------------- |
| `write(content: str)`                                 | Append raw HTML/text to system-output buffer                                     |
| `markdown(md_text: str)`                              | Render Markdown via Python-Markdown                                              |
| `latex(math_text: str)`                               | Render LaTeX math via MathJax                                                     |
| `error(msg: str)`                                     | Output red-styled error message                                                   |
| `warning(msg: str)`                                   | Output orange-styled warning                                                      |
| `success(msg: str)`                                   | Output green-styled success                                                       |
| `info(msg: str)`                                      | Output blue-styled info                                                           |
| `plt_plot(fig: matplotlib.figure.Figure)`             | Embed a Matplotlib figure                                                         |
| `plotly_plot(fig: plotly.Figure)`                     | Embed a Plotly figure                                                             |

---

## License

MIT © Bob Bobga Nti
