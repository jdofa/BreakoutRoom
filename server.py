import socket
import threading
import queue

# globals
msgs = queue.Queue() #used to distribute message as they come
history = [] #save chat history (list of text)
clients = [] #holds addresses of clients (list of tuples (IP, port))
# defining the port number of the instructor client
profAddress = "9000"
# AF_INET is the address family (default), in our case internet socket
# SOCK_DGRAM is the type of socket, in our case UDP
# server will be assigned a new socket (internet socket, UDP)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server will have a hostname of "localhost" and a port number of 9999
# we bind this information to the server socket
server.bind(("localhost", 9999))

# display the server is active
print("SERVER LISTENING ON PORT:9999")

def rcv(): #as we receive new messages, we add them to our queue and save them in history list
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
                    if "CLIENT_ADDED: " not in data:
                        server.sendto(data.encode(), address)




            for client in clients: #sends msg to all clients but themselves
                if client != address:
                    try:
                        #addy = (address[1]) #this allows us to access the specific port# (possibly allows us to assign specific access to certain people)
                        #server.sendto(f"{addy} HELP".encode(), client)
                        if msg.decode().startswith("CLIENT_ADDED: "): #notify when new client joins
                            username = msg.decode()[msg.decode().index(":")+1:]
                            server.sendto(f'{username} joined the server!'.encode(), client)
                            server.sendto(f'Private message ID: {address[1]}'.encode(), client)
                        else: #if its established client, then send their message
                            targetPort = msg.decode()[msg.decode().index("(")+11:msg.decode().index(")")+10]
                            if msg.decode().startswith("TO(",msg.decode().index("(")+8):        #THIS WORKS FINALLY
                                if int(targetPort)==int(client[1]):    #should be if targetPort == client[1]
                                    server.sendto(msg, client)
                                                                          #prevents message from being duplicated million times
                            else:
                                server.sendto(msg, client)
                    except:
                        clients.remove(client)

thread1 = threading.Thread(target=rcv)
thread2 = threading.Thread(target=send)

thread1.start()
thread2.start()

