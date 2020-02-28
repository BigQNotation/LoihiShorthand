from tkinter import *
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from queue import Queue

class DesktopApp:
    
    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.graphTimer = 20
        self.q = Queue(maxsize=10000)
        self.xPoint, self.yPoint = [], []
        self.fig, self.myPlt = plt.subplots()
        
        
    def setupWindow(self):
        self.frameWidth = 900
        self.frameHeight = 900
        self.root.title("Intel Loihi Shorthane")
        self.root.minsize(self.frameWidth, self.frameHeight)
        self.root.maxsize(self.frameWidth, self.frameHeight)
        self.root.resizable(0,0)
        self.graphSetup()

    def graphSetup(self):
        print("graphSetup")
        #self.myPlt.show()
        plt.ion()
        plt.xlim(100, 1200)
        plt.ylim(100, 1200)
        

    def graphPipe(self, conn):
        print("Graph Pipe")
        while(1):
            msg = conn.recv()
            print("openPipe: ", msg)
            self.q.put(msg)
            if(msg == "exit"): 
                break
        self.graphUpdate()
        self.doAfter(conn)

    def graphUpdate(self):
        print("graphUpdate")

        while(self.q.empty() == False):
            newData = self.q.get()
            print("newData: ", newData)
            print("self.xPoint: ", len(self.xPoint))
            print("self.yPoint: ", len(self.yPoint))
            self.xPoint.append(newData[0])
            self.yPoint.append(newData[1])
            if (self.q.empty()):
                print("empty q")
            

        self.graphStuff()

    def graphStuff(self):
        #
        plt.clf()
        
        plt.scatter(self.xPoint, self.yPoint, s=50, marker='x') #zorder, 
        plt.show()
        plt.pause(0.000001)

        #Stops at show ==============================
        #self.myPlt.scatter(self.xPoint, self.yPoint)
        #plt.show()

    def startUI(self):
        self.setupWindow()

    def getRoot(self):
        return self.root    

    def getQ(self):
        return self.q    

    def doAfter(self, conn):
        self.root.after(self.graphTimer,self.graphPipe,(conn))