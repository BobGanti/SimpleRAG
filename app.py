import syntaxmatrix as smx

# Enable dynamic theme toggle.
smx.enable_theme_toggle()

# Set theme and UI mode.
smx.set_theme("light")          # Options: "light" or "dark"
smx.set_ui_mode("bubble")       # Options: "bubble", "card", or "default"

# Register sidebar widgets.
smx.sidebar_text_input("sidebar_input", "Sidebar Input:", placeholder="Type here...")
smx.sidebar_button("sidebar_btn", "Do Sidebar Action", callback=lambda: smx.write("Sidebar action executed."))

def process_query():
    query = smx.get_text_input_value("user_query", default="What is RAG?")
    history = smx.get_chat_history()
    history.append(("User", query))
    response = f"Response to: {query}"
    history.append(("Bot", response))
    smx.set_chat_history(history)
    smx.clear_text_input_value("user_query")

def clear_chat():
    smx.clear_chat_history()

smx.set_widget_position("bottom")
smx.text_input("user_query", "Enter your RAG query:", placeholder="What is RAG?")
smx.button("submit_query", "Submit Query", callback=process_query)
smx.button("clear_chat", "Clear Chat", callback=clear_chat)

if __name__ == "__main__":
    smx.run()
