#!/usr/bin/python3

import multiprocessing
from multiprocessing import Pipe, Pool, Process, Queue
from socket import *
from tkinter import *


import matplotlib.pyplot as plt
import _thread
import DesktopApplication
from DesktopApplication import DesktopApp

DA = DesktopApp()

SERVER_PORT = 65000
BUFFER_SIZE = 1024
NUM_OF_CLIENTS = 10

#runs the UI Process
def UImain(UIConn):
    DA.startUI()
    deskApp = DA.getRoot()
    DA.doAfter(UIConn)
    deskApp.mainloop()

#Pipe end for the server
def dataReceived(data, serverConn):
    sData = data.split(']\n[')

    for x in range(len(sData)):
        #replace used to turn string into a number.
        sData[x] = sData[x].replace('[', '')
        sData[x] = sData[x].replace(']\n', '')
        sPair = sData[x].split(',')
        serverConn.send(sPair)

        #openPipe(sPair)

    serverConn.send("exit")
    #print("Data received: ", data)
    return

def sendResponse(connectionSocket):
    connectionSocket.send('Data received.\n'.encode('utf-8'))


def myThread(connectionSocket, addr, serverConn):

    print('Client connected from IP/PORT {}'.format(addr))
    while True:
        try:
            request = connectionSocket.recv(BUFFER_SIZE).decode()
        except Exception:
            print('Client disconnected from IP/PORT {}'.format(addr))
            connectionSocket.close()
            return

        if request:
            dataReceived(request, serverConn)

            # Send a response if "-1.0" string is received from phone client,
            # indicating that gesture is finished / "touch up" event occured
            sData = request.split(']\n[')
            for x in range(len(sData)):
                sData[x] = sData[x].replace('[', '')
                sData[x] = sData[x].replace(']\n', '')
                sPair = sData[x].split(',')
                if (sPair[0] == "-1.0"):
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


#server process is running here
def serverMain(serverConn):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((getLocalIPaddress(), SERVER_PORT))
    serverSocket.listen(NUM_OF_CLIENTS)
    print('Loihi server running on IP/PORT {}'.format(serverSocket.getsockname()))
    while True:
        connectionSocket, addr = serverSocket.accept()
        _thread.start_new_thread(myThread, (connectionSocket, addr, serverConn))

#new Main function for splitting the processes to a server and desktop application
def main():
    serverConn, UIConn = multiprocessing.Pipe()

    UI = multiprocessing.Process(name='UI', target=UImain, args=(UIConn,))
    serverM = multiprocessing.Process(name='Server', target=serverMain, args=(serverConn,))

    UI.start()
    serverM.start()

    UI.join()
    serverM.join()

if __name__=="__main__":
     main()
