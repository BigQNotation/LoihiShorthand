#!/usr/bin/python3

from socket import *
import _thread

IP_ADDRESS = "192.168.0.110"
SERVER_PORT = 65000
BUFFER_SIZE = 1024
NUM_OF_CLIENTS = 10

def dataReceived(data):
    # Do something with data
    print("Data received: %s", data)
    return

def sendResponse(connectionSocket):
    connectionSocket.send('Data received.'.encode('utf-8'))



def myThread(connectionSocket, addr):
    
    print('Client connected from IP/PORT {}'.format(addr))
    while True:
        try:
            request = connectionSocket.recv(BUFFER_SIZE).decode()
        except:
            print('Client disconnected from IP/PORT {}'.format(addr))
            connectionSocket.close()
            return

        if request:
            dataReceived(request)
            sendResponse(connectionSocket)
    

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((IP_ADDRESS, SERVER_PORT))
    serverSocket.listen(NUM_OF_CLIENTS)
    print('The server is running...')
    while True:    
        connectionSocket, addr = serverSocket.accept()
        _thread.start_new_thread(myThread, (connectionSocket, addr))


if __name__=="__main__":
    main()