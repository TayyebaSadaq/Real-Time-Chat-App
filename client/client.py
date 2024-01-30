# IMPORT MODULES
import socket
import threading 
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox # FOR WARNINGS AND ERRORS
import logging 
from encryption_utils import encrypt_message
import emoji_utils
from emoji_utils import EMOJI_MAPPING, show_emoji_options, on_key_press, insert_selected_emoji


## FOR DEBUGGING ##
logging.basicConfig(filename='encrypted_messages.log', level=logging.DEBUG)

# COLOURS AND FONTS
BLUSH = "#DF5D86"
PALE = "#E27092"
CHARM = "#EB92A9"
METALLIC = "#F1ABB9"
MYSTIC = "#D14F7B"
OFF_WHITE = "#f5eceb"

FONT = ("Times New Roman", 15)
SMALL_FONT = ("Times New Roman", 10)


## MAKING THESE GLOBAL VARIABLES ##
PORT = 1234
HOST = socket.gethostbyname(socket.gethostname())
   
# CREATING SOCKET OBJ
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# UPDATE THE MIDDLE FRAME WIDGET WITH MESSAGE
def update_msg_box(msg):
    # ADJUST MESSAGE BOX
    MESSAGE_BOX.config(state=tk.NORMAL) # ENABLED SO USER CAN TYPE IN IT
    MESSAGE_BOX.insert(tk.END, msg + "\n") # INSERT MESSAGE
    MESSAGE_BOX.config(state=tk.DISABLED) # DISABLED SO USER CANNOT TYPE IN IT

# CONNECT TO SERVER
def connect():
    global server_public_key

    try:
        client.connect((HOST, PORT))
        server_public_key = client.recv(2048).decode('utf-8')
        update_msg_box("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("UNABLE TO CONNECT TO SERVER", f"Unable to connect to server {HOST} {PORT}")

    username = USERNAME_TEXTBOX.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("INVALID USERNAME", "Username cannot be empty!")
        exit(0)

    threading.Thread(target=listen_msg, args=(client,)).start()

    USERNAME_TEXTBOX.config(state=tk.DISABLED)
    USERNAME_BUTTON.config(state=tk.DISABLED)
    
# # # SEND MESSAGE TO SERVER
def send_msg():
    message = MESSAGE_TEXTBOX.get()
    if message != '':
        if message.startswith('/exit'):
            encrypted_msg = encrypt_message(message, server_public_key)
            client.sendall(encrypted_msg)
            root.destroy()  # Close the tkinter window
        elif message.endswith(":"):
            show_emoji_options(MESSAGE_TEXTBOX, insert_selected_emoji)
        else:
            encrypted_msg = encrypt_message(message, server_public_key)
            client.sendall(encrypted_msg)
            MESSAGE_TEXTBOX.delete(0, len(message))
    else:
        messagebox.showerror("Message is empty")


## DEBUG IF MESSAGES ARE ENCRYPTED ##
# Modify the send_msg function
# def send_msg():
#     message = MESSAGE_TEXTBOX.get()
#     if message != '':
#         if message.startswith('/exit'):
#             encrypted_msg = encrypt_message(message, server_public_key)
#             logging.debug(f"Encrypted message: {encrypted_msg}")
#             client.sendall(encrypted_msg)
#             root.destroy()  # Close the Tkinter window
#         else:
#             encrypted_msg = encrypt_message(message, server_public_key)
#             logging.debug(f"Encrypted message: {encrypted_msg}")
#             client.sendall(encrypted_msg)
#             MESSAGE_TEXTBOX.delete(0, len(message))
#     else:
#         messagebox.showerror("Message is empty")


# USED TO CREATE TKINTER WINDOW
root = tk.Tk()

# WIDTH AND HEIGHT OF WINDOW
root.geometry("600x800")
root.title("Chatroom")
root.resizable(False, False) # NOT RESIZEABLE BY USER (X, Y)

# WEIGHTS FOR TKINTER WINDOW (ROWS AND COLUMNS) TO LOOK GOOD WHEN NO USERNAMES ARE ENTERED
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

# SPACES FOR TKINTER WINDOW
TOP_FRAME = tk.Frame(root, width=600, height=75, bg=PALE)
TOP_FRAME.grid(row=0, column=0, sticky=tk.NSEW) # FRAME STUCK TO TOP OF WINDOW

MIDDLE_FRAME = tk.Frame(root, width=600, height=650, bg=METALLIC)
MIDDLE_FRAME.grid(row=1, column=0, sticky=tk.NSEW) # FRAME STUCK TO TOP OF WINDOW

BOTTOM_FRAME = tk.Frame(root, width=600, height=75, bg=BLUSH)
BOTTOM_FRAME.grid(row=2, column=0, sticky=tk.NSEW) # FRAME STUCK TO TOP OF WINDOW

# WIDGETS FOR TOP FRAME

### USERNAME ENTRY ###
USERNAME_LABEL = tk.Label(TOP_FRAME, text="ENTER USERNAME: ", font=FONT, bg=PALE, fg=OFF_WHITE)
USERNAME_LABEL.pack(side=tk.LEFT, padx=10, pady=10)

USERNAME_TEXTBOX = tk.Entry(TOP_FRAME, font=FONT, bg=OFF_WHITE, fg=MYSTIC, width=30)
USERNAME_TEXTBOX.pack(side=tk.LEFT, padx=7, pady=10)

USERNAME_BUTTON = tk.Button(TOP_FRAME, text="Connect", font=SMALL_FONT, bg=PALE, fg=OFF_WHITE, command=connect)
USERNAME_BUTTON.pack(side=tk.LEFT, padx=9, pady=10)

# WIDGET FOR BOTTOM FRAM

### TEXT BOX FOR MESSAGES ###
MESSAGE_TEXTBOX = tk.Entry(BOTTOM_FRAME, font=FONT, bg=OFF_WHITE, fg=MYSTIC, width=50)
MESSAGE_TEXTBOX.pack(side=tk.LEFT, padx=10, pady=10)
MESSAGE_TEXTBOX.bind("<Key>", lambda event: on_key_press(event, MESSAGE_TEXTBOX))

MESSAGE_BUTTON = tk.Button(BOTTOM_FRAME, text="Send", font=SMALL_FONT, bg=PALE, fg=OFF_WHITE, width=6, height=2, command=send_msg)
MESSAGE_BUTTON.pack(side=tk.LEFT, padx=10, pady=10)

# WIDGETS FOR MIDDLE FRAME

## MIDDLE FRAME TEXT BOX FOR ALL MESSAGES ##
MESSAGE_BOX = scrolledtext.ScrolledText(MIDDLE_FRAME, font=SMALL_FONT, bg=OFF_WHITE, fg=MYSTIC, width=93, height=45, )
MESSAGE_BOX.config(state=tk.DISABLED) # DISABLED SO USER CANNOT TYPE IN IT
MESSAGE_BOX.pack(side=tk.LEFT, padx=10, pady=10)


# LISTEN FOR MESSAGES
# RUN AS THREAD TO KEEP LISTENING FOR MESSAGES
def listen_msg(client):
    while True:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            if msg.startswith('[SERVER]'):
                if "You have been kicked" in msg:
                    messagebox.showinfo("Kicked", msg)
                    client.close()
                    root.destroy()  # Close the tkinter window - KICKED
                else:
                    root.after(1, update_msg_box, msg)  # Schedule the update in the main thread
            elif msg.startswith('/exit'):
                exit_msg = "[SERVER] You have left the chat."
                messagebox.showinfo("Exit", exit_msg)
                client.close()
                root.destroy()  # Close the tkinter window - EXIT
                break
            else:
                # Assuming other messages are in the format "username|content"
                try:
                    username, content = msg.split('|', 1)
                    root.after(1, update_msg_box, f"{username}: {content}")  # Schedule the update in the main thread
                except ValueError:
                    print("Received message has an unexpected format.")
        else:
            messagebox.showerror("Message is empty")

# MAIN FUNCTION
def main():
    # KEEP TKINTER WINDOW RUNNING
    root.mainloop()

if __name__ == "__main__":
    main()