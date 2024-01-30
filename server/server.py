# IMPORT MODULES
import socket 
import threading 
import encryption_utils
from encryption_utils import generate_key_pair, encrypt_message, decrypt_message

PORT = 1234
HOST = socket.gethostbyname(socket.gethostname())

LISTENER_LIMIT = 6
ACTIVE_CLIENTS = [] # CURRENT CONNECTED USERS

def kick_user(kick_username):
    kick_username = kick_username.strip().lower()  # Remove leading/trailing whitespace and make it lowercase
    for user in ACTIVE_CLIENTS:
        if user[0].lower() == kick_username:
            kick_msg = f"[SERVER] You have been kicked from the chat."
            send_msg(user[1], kick_msg)
            ACTIVE_CLIENTS.remove(user)
            user[1].close()
            break
    else:
        not_found_msg = f"[SERVER] User {kick_username} not found in the chat."
        send_msg(kick_username, not_found_msg)


# KEEP RUNNING AND LISTENING FOR MESSAGES
def listen_msg(client, username, private_key):
    while True:
        try:
            encrypted_msg = client.recv(2048).decode('utf-8')
            decrypted_msg = decrypt_message(encrypted_msg, private_key)
        except ConnectionResetError:
            print(f"Connection with {username} reset by the remote host.")
            break
        except ConnectionAbortedError:
            print(f"Connection with {username} aborted by the software in the host machine.")
            break
        if not decrypted_msg:
            print(f"Connection with {username} closed by the remote host.")
            break

        if decrypted_msg.startswith('/exit'):  # IF MESSAGE STARTS WITH /EXIT
            exit_msg = f"[SERVER] {username} has left the chat."
            broadcast(exit_msg)
            client.close()
            break
        elif decrypted_msg.startswith('/kick'):  # IF MESSAGE STARTS WITH /KICK
            kick_target = decrypted_msg.split()[1]
            if username == kick_target:
                send_msg(client, "[SERVER] You cannot kick yourself.")
            else:
                kick_user(kick_target)
        else:
            final_msg = username + '|' + decrypted_msg
            broadcast(final_msg)



# SEND MESSAGE - SINGLE CLIENT
def send_msg(client, message):
    if isinstance(message, str):
        message = message.encode()  # Encode if it's a string
    client.sendall(message)



# BROADCAST MESSAGE TO USERS
def broadcast(message):
     
     for user in ACTIVE_CLIENTS:
         send_msg(user[1], message)
 
# HANDLE CLIENT
def handle(client):
    # Generate RSA key pair
    private_key, public_key = generate_key_pair()

    # Send public key to the client
    send_msg(client, public_key)

    # SERVER LISTEN FOR CLIENT MESSAGE CONTAINING USERNAME
    while True:
        username = client.recv(2048).decode('utf-8')  # DECODE MESSAGE WHEN RECEIVED
        if username != '':
            ACTIVE_CLIENTS.append((username, client))
            prompt_msg = "[SERVER]| Welcome to the chatroom " + username
            broadcast(prompt_msg)
            break
        else:
            print("Client username is empty!")

    threading.Thread(target=listen_msg, args=(client, username, private_key)).start()


# MAIN FUNCTION
def main():
    
    # CREATING SOCKET CLASS OBJ
    # AF_INET - USING IPv4 ADDRESSES
    # SOCK_STREAM - TCP PACKETS FOR COMMUNICATION
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print(f"Running the server on {HOST} {PORT}")
    
    # BINDING
    try:
        server.bind((HOST, PORT)) # PROVIDE SERVER WITH ADDRESS - HOST IP AND PORT
    except: # SOCKET CANNOT BIND TO HOST/PORT
        print(f"Unable to bind to host {HOST} and port {PORT}")
        
    # SET SERVER LIMIT
    server.listen(LISTENER_LIMIT)

    # KEEP LISTENING FOR CLIENT CONNECTIONS
    while True:
        client, address = server.accept()
        print(f"Successful connection to client: {address[0]} {address[1]}") # PRINT HOST AND PORT OF CLIENT
        
        threading.Thread(target = handle, args = (client, )).start() # WHEN CLIENT CONNECTS, NEW THREAD CREATED
        
if __name__ == "__main__":
    main()
    