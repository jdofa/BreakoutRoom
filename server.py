import socket
import threading

host = '127.0.0.1' #localhost
port = 30000 #make sure to use port that isn't popular

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.socket(specifies internet socket, specifies using TCP over UDP)
server.bind((host,port)) 
server.listen() #wait for client to connect

clients = []
usernames = []

#sends message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#handles the messages sent by clients
def handle(client):
    while True:
        try: #sends message recieved by client to chatroom
            message = client.recv(1024)
            broadcast(message)
        except: #handles a client disconnecting
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} left the chatroom!'.encode('ascii'))
            usernames.remove(username)
            break

#handles receiving new clients
def receive():
    while True:
        client, address = server.accept() #accepts client, stores variables accordingly
        print(f"Connected with {str(address)}")

        client.send('Username:'.encode('ascii')) #asks client for username
        username = client.recv(1024).decode('ascii') #storing given username
        usernames.append(username)
        clients.append(client)

        print(f'Your username is {username}!') #lets client know their username
        broadcast(f'{username} joined the room!'.encode('ascii')) #lets everyone in the server know who joined with given username
        client.send('Connected to the server!'.encode('ascii')) #lets client know they are connected to the server

        #thread that runs handle function
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
#calling receive function to start procedure        
receive()