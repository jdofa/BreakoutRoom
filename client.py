import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (internet socket, UDP)
port = random.randint(8000,9000)
client.bind(("localhost", port)) #when presenting, no need to specify different ports
username = input("Enter a username: ")

def rcv(): #handles recieving messages from server and prints them
    while True:
        try:
            msg, _ = client.recvfrom(1024)
            print(msg.decode())
        except:
            pass

thread1 = threading.Thread(target=rcv)
thread1.start()

client.sendto(f"CLIENT_ADDED:{username}".encode(), ("localhost", 9999)) #specifies new client so server can notify everyone that new client joined

while True: #send user input to server
    msg = input("")
    if msg == "quit":
        exit()
    else:
        client.sendto(f'{username}: {msg}'.encode(), ("localhost", 9999))

