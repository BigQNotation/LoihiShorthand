from tkinter import *
import matplotlib
from queue import Queue

class DesktopApp:
    
    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.graphTimer = 2000
        self.q = Queue(maxsize=100)
        
        
    def setupWindow(self):
        print("Window Start")
        self.frameWidth = 900
        self.frameHeight = 900
        self.root.title("Intel Loihi Shorthane")
        self.root.minsize(self.frameWidth, self.frameHeight)
        self.root.maxsize(self.frameWidth, self.frameHeight)
        self.root.resizable(0,0)

    def graphPipe(self, desktopConn, data):
        msg = "Connection with Desktop Sessionful"
        desktopConn.send(msg)
        print("Incoming Data: ", data)
        self.q.put(data)
        desktopConn.close()

    def graphUpdate(self):
        print("GraphUpdate start\n")
        print("q.empty(): ", self.q.empty())
        while (self.q.empty() != True):
            print("q.get(): ", self.q.get())
        self.root.after(self.graphTimer, self.graphUpdate)

    def startUI(self):
        self.setupWindow()
        print("Setup Complete")
        self.root.after(self.graphTimer, self.graphUpdate)
        print("Should be running Mainloop at this point?")
        #self.root.mainloop()

    def getRoot(self):
        return self.root





