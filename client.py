import socket
import threading
import struct
import random

mcastPort = 9999
mcastGroup = '224.3.2.1'
clientIP = socket.gethostbyname(socket.gethostname()) #grabs clients ip address
serverIP = '10.0.0.44' #need to hardcode the server's IP
username = input("Enter a username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.bind((clientIP, mcastPort)) 
mreq = struct.pack("4sl", socket.inet_aton(mcastGroup), socket.INADDR_ANY)
client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def rcv(): #handles recieving messages from server and prints them
    while True:
        try:
            msg, _ = client.recvfrom(1024) #used to print history
            print(msg.decode())
        except:
            pass

thread1 = threading.Thread(target=rcv)
thread1.start()

client.sendto(f"CLIENT_ADDED:{username}".encode(), (serverIP, 8888)) #specifies new client so server can notify everyone that new client joined

while True: #send user input to server
    msg = input("")
    if msg == "quit":
        exit()
    else:
        client.sendto(f'{username}: {msg}'.encode(), (serverIP, 8888))

