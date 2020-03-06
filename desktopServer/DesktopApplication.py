from tkinter import *
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from queue import Queue

class DesktopApp:
    
    #initates the class
    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.graphTimer = 20
        self.q = Queue(maxsize=10000)
        self.xPoint, self.yPoint = [], []
        self.fig = plt.figure()
        #self.myPlt = plt.subplots()
        
    #Setup the window to specific size
    def setupWindow(self):
        self.frameWidth = 900
        self.frameHeight = 900
        self.root.title("Intel Loihi Shorthand")
        self.root.minsize(self.frameWidth, self.frameHeight)
        self.root.maxsize(self.frameWidth, self.frameHeight)
        self.root.resizable(0,0)
        self.graphSetup()

    #Sets up the baiscs for the graph
    def graphSetup(self):
        print("graphSetup")
        #self.myPlt.show()
        plt.ion()
        plt.xlim(100, 1200)
        plt.ylim(100, 1200)
        

    #Takes the incoming information from the pip and adds it to the internal queue = q 
    def graphPipe(self, conn):
        print("Graph Pipe")
        while(1):
            msg = conn.recv()
            print("openPipe: ", msg)
            if(msg == "exit"): 
                break
            else:
                self.q.put(msg)
        self.graphUpdate()
        self.doAfter(conn)

    #Processes the information from the q and adds it to the graphing data sets x and y
    def graphUpdate(self):
        print("graphUpdate")

        while(self.q.empty() == False):
            newData = self.q.get()
            #print("newData: ", newData)
            #print("self.xPoint: ", len(self.xPoint))
            #print("self.yPoint: ", len(self.yPoint))
            if(float(newData[0]) != -1.0):
                print("New Data Added")
                self.xPoint.append(float(newData[0]))
                self.yPoint.append(float(newData[1]))
            else:
                self.saveGraph()
        self.graphStuff()

    def saveGraph(self):
        print("saving graph")
        #self.fig = plt.figure()
        self.fig.savefig('plot.png')


    #Graphs the informations in the data sets x and y, shows them in a plot.  
    def graphStuff(self):
        self.fig = plt.gcf()
        plt.clf()
        plt.scatter(self.xPoint, self.yPoint, s=50, marker='o') 
        plt.plot(self.xPoint, self.yPoint) #plot a line graph
        plt.show()
        plt.pause(0.000001)

        #Stops at show ==============================
        #self.myPlt.scatter(self.xPoint, self.yPoint)
        #plt.show()

    #Just runs the setupWindows() file.
    def startUI(self):
        self.setupWindow()

    #Returns the root so the mainloop run in the server file.
    def getRoot(self):
        return self.root    

    #returns a q to the server
    def getQ(self):
        return self.q    

    #nessary for the graphPipe to trigger after the mainloop() for the desktop application.
    def doAfter(self, conn):
        self.root.after(self.graphTimer,self.graphPipe,(conn))