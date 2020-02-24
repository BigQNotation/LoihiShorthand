#!/usr/bin/python3

from socket import *
import _thread
import multiprocessing
from multiprocessing import Pool, Process, Queue, Pipe
import DesktopApplication
from DesktopApplication import DesktopApp

DA = DesktopApp()

SERVER_PORT = 65000
BUFFER_SIZE = 1024
NUM_OF_CLIENTS = 10

def openPipe(data):
    serverConn, desktopConn = Pipe()
    p = Process(target=DA.graphPipe, args=(desktopConn,data,))
    p.start()
    print(serverConn.recv())

def dataReceived(data):
    # Do something with data
    # data example: [491.00717, 558.7286]
    sData = data.split(']\n[') 
    
    for x in range(len(sData)): 
        #replace used to turn string into a number.
        sData[x] = sData[x].replace('[', '') 
        sData[x] = sData[x].replace(']\n', '')
        sPair = sData[x].split(',') 
        openPipe(sPair)

    print("Data received: ", data)
    return

def sendResponse(connectionSocket):
    connectionSocket.send('Data received.'.encode('utf-8'))

def myThread(connectionSocket, addr):    
    print('Client connected from IP/PORT {}'.format(addr))
    while True:
        try:
            request = connectionSocket.recv(BUFFER_SIZE).decode()
        except Exception:
            print('Client disconnected from IP/PORT {}'.format(addr))
            connectionSocket.close()
            return

        if request:
            dataReceived(request)
            sendResponse(connectionSocket)

# Returns current IP address assigned to local machine
def getLocalIPaddress():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
    except Exception:
        print('Local machine in not connected to any network!')
        print('Loihi Server could not start.')
        exit()
    return s.getsockname()[0]  

def UImain():
    DA.startUI()
    deskApp = DA.getRoot()
    deskApp.mainloop()

def serverMain():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)    
    serverSocket.bind((getLocalIPaddress(), SERVER_PORT))
    serverSocket.listen(NUM_OF_CLIENTS)
    print('Loihi server running on IP/PORT {}'.format(serverSocket.getsockname()))
    while True:
        connectionSocket, addr = serverSocket.accept()
        _thread.start_new_thread(myThread, (connectionSocket, addr))

def main():    
    #pool = Pool(processes=2)
    UI = multiprocessing.Process(name='my_service', target=UImain)
    serverM = multiprocessing.Process(name='my_service', target=serverMain)
    
    UI.start()
    serverM.start()

    #serverSocket = socket(AF_INET, SOCK_STREAM)
    #serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)    
    #serverSocket.bind((getLocalIPaddress(), SERVER_PORT))
    #serverSocket.listen(NUM_OF_CLIENTS)
    #print('Loihi server running on IP/PORT {}'.format(serverSocket.getsockname()))
    #while True:
    #    connectionSocket, addr = serverSocket.accept()
    #    _thread.start_new_thread(myThread, (connectionSocket, addr))

if __name__=="__main__":
     main()
