from tkinter import *
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from queue import Queue
import datetime

import csv
import os


class DesktopApp:

    # initates the class
    def __init__(self):
        super().__init__()
        # create new folder
        self.root = Tk()
        self.graphTimer = 20
        self.q = Queue(maxsize=10000)
        self.xPoint, self.yPoint = [], []
        self.fig = plt.figure()
        # self.myPlt = plt.subplots()

    # Setup the window to specific size
    def setupWindow(self):
        self.frameWidth = 900
        self.frameHeight = 900
        self.root.title("Intel Loihi Shorthand")
        self.root.minsize(self.frameWidth, self.frameHeight)
        self.root.maxsize(self.frameWidth, self.frameHeight)
        self.root.resizable(0, 0)
        self.graphSetup()

    # Sets up the baiscs for the graph
    def graphSetup(self):
        print("graphSetup")
        # self.myPlt.show()
        plt.ion()
        plt.xlim(100, 1200)
        plt.ylim(100, 1200)

    # Takes the incoming information from the pip and adds it to the internal queue = q
    def graphPipe(self, conn):
        print("Graph Pipe")
        now = datetime.datetime.now()
        dt_string = now.strftime("%d_%m_%Y__%S_%M_%H")
        os.makedirs("graphs", exist_ok=True)
        gph_string = "graphs/" + dt_string
        self.gph_string = gph_string
        os.makedirs(gph_string, exist_ok=True)
        csvfile = open(gph_string + '/data.csv', 'a')
        self.csvfile = csvfile
        csvWriter = csv.writer(csvfile)
        csvwriter = csvWriter
        while 1:
            msg = conn.recv()
            print("openPipe: ", msg)
            self.graphStuff()
            if msg[0] == '-1.0':
                self.saveGraph()
                break
            else:
                print(msg)
                print(" is added to queue\n")
                self.xPoint.append(float(msg[0]))
                self.yPoint.append(float(msg[1]))
                plt.draw()
            csvwriter.writerow([float(msg[0]), float(msg[1])])
        self.doAfter(conn)

    # Processes the information from the q and adds it to the graphing data sets x and y


    def saveGraph(self):
        print("saving graph")
        # self.fig = plt.figure()
        saveloc = self.gph_string + '/plot.png'
        self.fig.savefig(saveloc)
        self.csvfile.close()
        self.xPoint, self.yPoint = [], []

    # Graphs the informations in the data sets x and y, shows them in a plot.
    def graphStuff(self):
        self.fig = plt.gcf()
        plt.clf()
        plt.scatter(self.xPoint, self.yPoint, s=50, marker='o')
        plt.plot(self.xPoint, self.yPoint)  # plot a line graph
        plt.show()
        plt.pause(0.000001)

        # Stops at show ==============================
        # self.myPlt.scatter(self.xPoint, self.yPoint)
        # plt.show()

    # Just runs the setupWindows() file.
    def startUI(self):
        self.setupWindow()

    # Returns the root so the mainloop run in the server file.
    def getRoot(self):
        return self.root

        # returns a q to the server

    def getQ(self):
        return self.q

        # nessary for the graphPipe to trigger after the mainloop() for the desktop application.

    def doAfter(self, conn):
        self.root.after(self.graphTimer, self.graphPipe, (conn))
