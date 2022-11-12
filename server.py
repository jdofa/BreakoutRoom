import socket
import threading
import queue

msgs = queue.Queue() #used to distribute message as they come
history = [] #save chat history
clients = [] #holds addresses of clients
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

def rcv(): #as we recieve new messages, we add them to our queue and save them in history list
    while True:
        try:
            msg, address = server.recvfrom(1024)
            msgs.put((msg, address))
            history.append(msg.decode())
        except:
            pass

def send(): #handles sending msgs as they arrive
    while True:
        while not msgs.empty(): #as the queue is filled, distribute message
            msg, address = msgs.get()
            print(msg.decode())

            if address not in clients: #if new client, add their address to our list
                clients.append(address)

                for data in history: #sends history to new client
                    if "CLIENT_ADDED:" not in data:
                        server.sendto(data.encode(), address)

            for client in clients: #sends msg to all clients but themselves
                if client != address:
                    try:
                        if msg.decode().startswith("CLIENT_ADDED:"): #notify when new client joins
                            username = msg.decode()[msg.decode().index(":")+1:]
                            server.sendto(f'{username} joined the server!'.encode(), client)
                        else: #if its established client, then send their message
                            server.sendto(msg, client)
                    except:
                        clients.remove(client)

thread1 = threading.Thread(target=rcv)
thread2 = threading.Thread(target=send)

thread1.start()
thread2.start()


