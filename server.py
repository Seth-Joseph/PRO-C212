import socket
from threading import Thread
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

IP_ADDRESS = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096
clients = {}

def handleClient(client,client_name):
    pass

def acceptConnections():
    global SERVER
    global clients

    while True:
        client,addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client" :client,
            "address":addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4096
        }
        print(f"connected with {client_name}:{addr}")

        thread = Thread(target = handleClient,args=(client,client_name))
        thread.start()

def setup():
    print('\t\t\t\t\t\tMUSIC SHARE')

    global SERVER
    global IP_ADDRESS
    global PORT

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))

    SERVER.listen(100)

    print("\t\t\t\t\tWAITING FOR CONNECTIONS")

    acceptConnections()


def ftp():
    global IP_ADDRESS

    autho = DummyAuthorizer()
    autho.add_user('root','password','.',perm='elradfmw')

    hand = FTPHandler
    hand.authorizer = autho

    serve = FTPServer((IP_ADDRESS,21),hand)
    serve.serve_forever()

setupThread = Thread(target=setup)
setupThread.start()

setupThread = Thread(target=ftp)
setupThread.start()