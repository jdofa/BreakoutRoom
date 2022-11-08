import socket
import threading

username = input("Choose your username: ")

host = '127.0.0.1' #localhost
port = 30000 #make sure to use port that isn't popular

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.socket(specifies internet socket, specifies TCP connection)
client.connect(('127.0.0.1', 30000)) #should be same as server (address, port)

#
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii') #message recieved from server
            if message == 'Username:': #if server asks for username
                client.send(username.encode('ascii')) #send the server your username
            else:
                print(message) #otherwise print whatever the server sent
        except:
            #if there is an excception, disconnect client
            print("An error occured! You have been disconnected.")
            client.close()
            break

def write():
    while True: #formatting and sending the message
        message = '{}: {}'.format(username, input('')) 
        client.send(message.encode('ascii')) 

#thread that handles recieving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#thread that handles sending messages
write_thread = threading.Thread(target=write)
write_thread.start()
