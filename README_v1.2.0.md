# syntaxmatrix UI Framework v1.2.0

**SyntaxMUI:** A customizable UI framework for Python AI assistant projects.

[![PyPI Version](https://img.shields.io/pypi/v/syntaxmatrix.svg)](https://pypi.org/project/syntaxmatrix)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Overview

`syntaxmatrix` (lowercase) is a lightweight, Pythonic UI library that lets you build interactive chat-style front-ends for AI apps without diving into a full web framework. It provides:

- Rapid widget registration (text inputs, buttons, file uploaders)
- Dynamic theme toggling and multiple UI modes
- Built-in PDF ingestion & chunking
- Stylized feedback (success, error, warning, info)
- Admin panel, session management, and more

Ideal for Retrieval-Augmented Generation (RAG) demos, data explorers, or any AI assistant interface.

---

## Quick Links

- **Documentation:** https://github.com/bobganti/SyntaxMatrix
- **PyPI:** `pip install syntaxmatrix==1.2.0`
- **Source:** https://github.com/bobganti/SyntaxMatrix

---

## Features

- **Rapid UI Creation**: One-line calls to register `text_input`, `button`, `file_uploader`, etc.
- **Built-in Chat Loop**: Core `/process_chat` endpoint automatically wires three keys:
  - `user_query` (text input),
  - `submit_query` (send button),
  - `user_pdfs` (PDF uploader + chunking).
- **Custom Widgets**: Register any keys you like—just provide matching handler logic.
- **PDF Ingestion**: `load_pdf_chunks(directory)` scans a folder, splits PDFs into chunks, caches in SQLite, and returns a `{filename: [chunks,…]}` map.
- **Session File Uploads**: `get_user_chunks()`, `add_user_chunks()`, `clear_user_chunks()` for per-session user files.
- **Dynamic Themes**: `enable_theme_toggle()`, `set_theme()`, plus `list_themes()`.
- **Multiple UI Modes**: `set_ui_mode()` supports `default`, `bubble`, `card`, **`smx`** (new!) and `list_ui_modes()`.
- **Rich Output**: `markdown()`, `latex()`, `plt_plot()`, `plotly_plot()`, plus `error()`, `warning()`, `success()`, `info()`.
- **Branding Helpers**: `set_user_icon()`, `set_bot_icon()`, `set_site_icon()`, `set_site_logo()`, `set_site_title()`, `set_project_title()`.
- **Session Management**: Named chat sessions with rename/delete; session IDs via `get_session_id()`.

---

## Installation

```bash
pip install syntaxmatrix==1.2.0
```

**Dependencies**

- Python >= 3.7
- Flask >= 2.0.0
- requests >= 2.0.0
- markdown >= 3.3.0
- matplotlib >= 3.5.0
- plotly >= 5.0.0
- openai >= 0.27.0
- PyPDF2 >= 1.26.0
- numpy >= 1.21.0

Optional extras:

```bash
# Transformer models & torch
pip install syntaxmatrix[advanced_nlp]

# pandas for data APIs
pip install syntaxmatrix[data]

# Testing
pip install syntaxmatrix[testing]
```

---

## Quick-Start Snippet

This minimal example uses the **built-in** chat flow (no custom keys required):

```python
import syntaxmatrix as smx

# Handler for text-submission
def create_conversation():
    q = smx.get_text_input_value("user_query").strip()
    if not q:
        smx.warning("Please enter a question.")
        return
    # …your AI call or logic here…
    smx.success(f"You asked: {q}")

# UI setup
smx.set_ui_mode("smx")               # new "smx" display style
smx.enable_theme_toggle()            # add light/dark toggle

# Activate built-in widgets (must use these keys)
smx.text_input(
    "user_query",                  # text box
    "Ask me anything…",            # label
    placeholder="Type your question here…"
)
smx.button(
    "submit_query",                # send button key
    "Send",                        # label
    callback=create_conversation    # invoked on send
)
smx.file_uploader(
    "user_pdfs",                   # PDF uploader key
    "Upload PDFs",                 # label
    accept_multiple_files=True     # chunking happens automatically
)

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

MIT © Bob Nti
