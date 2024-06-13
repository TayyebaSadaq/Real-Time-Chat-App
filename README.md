## 💬 RealTimeChatApp
This is a project from my second year - first semester in Networks and Security. The task was to produce an Internet of Things (IOT) application that demonstrates
- The ability to structure and comment code
- Client/server model and/or peer-to-peer model principles
- Communication security principles

## 🏆 The Result
The result is a python chat application that encrypts and decrypts messages via RSA . Made using the Tkinter module in python, the application creates a user interface for each client when connecting to the server. Allowing them to view any messages sent from when they joined as well as assign themseslves a name clearly. Along with the integration of emoji's using ":" in the chat box which shows a menu of the available options for the user to use to have a more exciting message.

## 📋 Pre-requisites
You'll need python installed as well as the following for the encryption <br/>

- run cmd:<br/>
- pip install rsa -> encrytption<br/>
- pip install pycrptodome -> encryption<br/>

^ to check that the encryption is working there is debugging active in the code that writes to the file "encrypted_messages.log"

---
To then run the application itself:<br/>

- open server in integrated terminal type: python server.py
- open client in integrated terminal type: python client.py

*repeat for as many clients as you want in the chatroom
