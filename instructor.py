import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (internet socket, UDP)
port = 9000
username = input("Enter a username: ")
client.bind(("localhost", 9000))

def rcv(): #handles recieving messages from server and prints them
    while True:
        try:
            msg, _ = client.recvfrom(1024)
            print(msg.decode())
            #print(f"this is a tuple: %s" % (_,))
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
        client.sendto(f'{username} (Instructor): {msg}'.encode(), ("localhost", 9999))

