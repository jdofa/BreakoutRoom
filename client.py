import socket
import threading
import random

# AF_INET is the address family (default), in our case internet socket
# SOCK_DGRAM is the type of socket, in our case UDP
# client will be assigned a new socket (internet socket, UDP)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# generating a random int port number from 8000-8999 for the client
port = random.randint(8000,8999)

# asking user to type a username for the client
username = input("Enter a username: ")

# when presenting, no need to specify different ports
# all clients will have a hostname of "localhost", but a different port (used for the AF_INET address family)
# we bind this information to the client socket
client.bind(("localhost", port)) 

def rcv(): #handles receiving messages from server and prints them
    while True:
        try:
            msg, _ = client.recvfrom(1024)
            print(msg.decode())
            #print(f"this is a tuple: %s" % (_,))
        except:
            pass

# define thread and start thread
thread1 = threading.Thread(target=rcv)
thread1.start()

# specifies new client so server can notify everyone that new client joined
client.sendto(f"CLIENT_ADDED: {username}".encode(), ("localhost", 9999))

while True: # handles sending user input to server
    # asking user client for input message to send to server
    msg = input("")
    # code removed
    #msg = input(f"{username}: ")
    #idx = msg.find(":")
    #msg = msg[idx + 1 : len(msg)]
    if msg == "quit":
        exit()
    else:
        # sending the message to the server
        client.sendto(f'{username}({port}): {msg}'.encode(), ("localhost", 9999))

