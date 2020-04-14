from tkinter import *
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from queue import Queue
import datetime

import csv
import os
from tempfile import TemporaryFile
import glob
#import cv2

class DesktopApp:

    # initates the class
    def __init__(self):
        super().__init__()
        # create new folder
        self.root = Tk()
        self.graphTimer = 20
        self.q = Queue(maxsize=10000)
        self.xPoint, self.yPoint = [], []
        #self.fig = plt.figure()
        self.trainingFileCount = 0;
        self.label_swapper = 0

        # used to create grayscale image array
        self.grayscale_image_array = []
        self.grayscale_image_array.append([])
        self.grayscale_image_array.append([])
        self.gia_fig = plt.figure()
        self.array_label_swapper = 0

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
        plt.axis('off')
        plt.axis('equal')
        #plt.axis('equal')
        #plt.gca().set_aspect('equal', adjustable='box')
        #plt.xlim(00, 3000)
        #plt.ylim(00, 3000)

    # Takes the incoming information from the pip and adds it to the internal queue = q
    def graphPipe(self, conn):
        print("Graph Pipe")
        msg = conn.recv()
        if msg[0] == '-1.0':
            self.doAfter(conn)
            return
        self.xPoint.append(float(msg[0]))
        self.yPoint.append(float(msg[1]))
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
            print("openPipe: ", msg)
            if msg[0] == '-1.0':
                self.saveGraph()
                break
            self.graphStuff()
            print(msg)
            print(" is added to queue\n")
            self.xPoint.append(float(msg[0]))
            self.yPoint.append(float(msg[1]))
            csvwriter.writerow([float(msg[0]), float(msg[1])])

            # gray scale image array implementation
            self.grayscale_image_array[0].append(float(msg[0]))
            self.grayscale_image_array[1].append(float(msg[1]))

            msg = conn.recv()
        self.doAfter(conn)

    # Processes the information from the q and adds it to the graphing data sets x and y


    def saveGraph(self):
        print("saving graph")

        '''
        # save graph to training location
        os.makedirs("training", exist_ok=True)
        training_directory = "training/"
        if (self.trainingFileCount < 10):
            training_saveloc = training_directory + '/plot0' + str(self.trainingFileCount) + '.png'
        if (self.trainingFileCount >= 10):
            training_saveloc = training_directory + '/plot' + str(self.trainingFileCount) + '.png'
        self.fig.savefig(training_saveloc)
        self.trainingFileCount = self.trainingFileCount + 1
        '''
        # modify grayscale image array to be offset
        # by its height. this operation is done
        # to make gestures similar grayscale values,
        # regardless of the area on the phone they're drawn.

        # find min x coordinate value
        x_coord_min = 100000
        for x_coord in self.grayscale_image_array[0]:
            if (x_coord < x_coord_min):
                x_coord_min = x_coord
        # offset all x coordinate values by min x
        for x_coord in self.grayscale_image_array[0]:
            x_coord = x_coord - x_coord_min

        # find min y coordinate value
        y_coord_min = 100000
        for y_coord in self.grayscale_image_array[1]:
            if (y_coord < y_coord_min):
                y_coord_min = y_coord
        # offset all y coordinate values by min x
        for y_coord in self.grayscale_image_array[1]:
            y_coord = y_coord - y_coord_min

        self.graphStuff()


        # save grayscale image array to training location
        os.makedirs("arraytraining", exist_ok=True)
        array_training_directory = "arraytraining/"
        if (self.trainingFileCount < 10):
            training_saveloc = array_training_directory + '/array0' + str(self.trainingFileCount) + '.png'
        if (self.trainingFileCount >= 10):
            training_saveloc = array_training_directory + '/array' + str(self.trainingFileCount) + '.png'
        self.gia_fig.savefig(training_saveloc)
        self.trainingFileCount = self.trainingFileCount + 1

        # clear the image array for next gesture
        self.grayscale_image_array = []
        self.grayscale_image_array.append([])
        self.grayscale_image_array.append([])



        # self.fig = plt.figure()
        '''
        saveloc = self.gph_string + '/plot.png'
        self.fig.savefig(saveloc)
        self.csvfile.close()
        self.xPoint, self.yPoint = [], []
        '''

        # save image and label to numpy binary files
        '''
        image_array = []
        label_array = []
        files = glob.glob(training_directory + '/*.PNG')
        for myFile in files:
            image = cv2.imread(myFile)
            dim = 20,20
            resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            resized_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            image_array.append(resized_gray)
            label_array.append(self.label_swapper % 3) # change mod to match amount of gestures to be trained
            self.label_swapper = self.label_swapper + 1
        np.save(training_directory + '/imageTrain',image_array)
        np.save(training_directory + '/labelTrain',label_array)
        '''

        # save grayscale image array and label to numpy binary files
        image_array = []
        label_array = []
        files = glob.glob(array_training_directory + '/*.PNG')
        for myFile in files:
            image = cv2.imread(myFile)
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image_array.append(image_gray)
            label_array.append(self.array_label_swapper % 3) # change mod to match amount of gestures to be trained
            self.array_label_swapper = self.array_label_swapper + 1
        np.save(array_training_directory + '/imageTrain',image_array)
        np.save(array_training_directory + '/labelTrain',label_array)


        plt.clf()

    # Graphs the informations in the data sets x and y, shows them in a plot.
    def graphStuff(self):
        '''
        self.fig = plt.gcf()
        plt.axis('off')
        plt.axis('equal')
        plt.plot(self.xPoint, self.yPoint, '-k', linewidth=5)  # plot a line graph
        plt.show()
        plt.pause(0.000001)
        '''

        self.gia_fig = plt.gcf()
        plt.axis('off')
        #plt.axis('equal')
        plt.imshow(self.grayscale_image_array, cmap="gray")
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
