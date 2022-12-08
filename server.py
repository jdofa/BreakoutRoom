import socket
import threading
import struct
import queue

msgs = queue.Queue() #used to distribute message as they come
history = [] #save chat history
clients = [] #holds addresses of clients
person = [] #(username, address) -> address = (ip, port)

mcastAddress = ('224.3.2.1', 9999)
mcastPort = 9999
mcastGroup = '224.3.2.1'
ttl = 1

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP) 
serverIP = socket.gethostbyname(socket.gethostname())
server.bind((serverIP, 8888))



def rcv(): #as we recieve new messages, we add them to our queue and save them in history list
    while True:
        try:
            msg, address = server.recvfrom(1024)
            msgs.put((msg, address)) #put msg with address into queue
            history.append(msg.decode()) #adding messages coming into server 
        except:
            pass

def send(): #handles sending msgs as they arrive
    while True:
        while not msgs.empty(): #as the queue is filled, distribute message
            msg, address = msgs.get()
            print(f'msg:{msg.decode()} address:{address}')

            if address not in clients: #if new client, add their address to our list
                clients.append(address)

                for data in history: #sends history to new client
                    if "CLIENT_ADDED:" not in data:
                        server.sendto(data.encode(), address)

            if msg.decode().startswith("CLIENT_ADDED:"): #notify when new client joins
                username = msg.decode()[msg.decode().index(":")+1:]
                person.append((username,address))
                server.sendto(f'{username} joined the server!'.encode(), mcastAddress)
            else:
                server.sendto(msg, mcastAddress)

thread1 = threading.Thread(target=rcv)
thread2 = threading.Thread(target=send)

thread1.start()
thread2.start()


