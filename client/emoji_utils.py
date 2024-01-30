import tkinter as tk
from tkinter import Listbox, Toplevel

EMOJI_MAPPING = {
    ":)": "😊",
    ":D": "😃",
    ":(": "😞",
}

emoji_window = None
emoji_listbox = None

def show_emoji_options(textbox, insert_selected_emoji):
    global emoji_window, emoji_listbox
    emoji_window = Toplevel(textbox.master)
    emoji_window.title("Emoji Options")

    emoji_listbox = Listbox(emoji_window, selectmode='single')
    for emoji_text in EMOJI_MAPPING.values():
        emoji_listbox.insert('end', emoji_text)

    emoji_listbox.pack()
    emoji_listbox.bind("<Double-Button-1>", lambda event: insert_selected_emoji(event, textbox))

def insert_selected_emoji(event, textbox):
    global emoji_window, emoji_listbox
    selected_index = emoji_listbox.curselection()
    if selected_index:
        selected_emoji = emoji_listbox.get(selected_index)
        current_text = textbox.get()
        cursor_position = textbox.index('insert')
        
        # Find the last occurrence of a colon in the message
        last_colon_index = current_text.rfind(":")
        
        # Replace the last colon with the selected emoji
        new_text = current_text[:last_colon_index] + selected_emoji + current_text[last_colon_index + 1:]
        
        # Update the textbox
        textbox.delete(0, tk.END)
        textbox.insert(0, new_text)
        
        # Move the cursor after the inserted emoji
        textbox.icursor(cursor_position - len(current_text) + len(new_text))
        
        # Destroy the emoji window
        emoji_window.destroy()

# Update the on_key_press function to use the modified insert_selected_emoji
def on_key_press(event, textbox):
    current_text = textbox.get()
    cursor_position = textbox.index('insert')

    if current_text.endswith(":"):
        show_emoji_options(textbox, insert_selected_emoji)
        textbox.icursor(cursor_position - 1)  # Move the cursor back to the original position
