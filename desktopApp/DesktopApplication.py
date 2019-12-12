#run by commandline  $ python3 DesktopApplication.py

from tkinter import *
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

#Size values
frameWidth = 1920 
frameHeight = 920

TAWidth = 182 #fit prefect in pycharm ran from terminal 130 fits better
TAHeight = 82 #fit prefect in pycharm ran from terminal 45 fits better


figSizeX = 6.375
figSizeY = 4.5

#basic window setup
root = Tk()
root.title("Intel Loihi ShortHand")
root.minsize(frameWidth, frameHeight)
root.maxsize(frameWidth, frameHeight)
root.resizable(0, 0)

#creates subframes 
rightFrame = LabelFrame(root, text="Translated Text", width=int(round(2 * frameWidth/3)), height=frameHeight, bg="blue")
leftTopFrame = LabelFrame(root, text="Drawn", width=int(round(frameWidth/3)), height=frameHeight / 2, bg="red")
leftBottomFrame = LabelFrame(root, text="Process", width=int(round(frameWidth/3)), height=frameHeight / 2, bg="white")

root.rowconfigure(0, weight=0)
root.columnconfigure(0, weight=0)

leftTopFrame.columnconfigure(0, weight=0)
leftBottomFrame.columnconfigure(0, weight=0)

leftTopFrame.rowconfigure(0, weight=0)
leftBottomFrame.rowconfigure(0, weight=0)

# rightFrame
TextArea = Text(rightFrame)
TextArea.config(width=TAWidth, height=TAHeight) #sets the size to fit the area 
TextArea.pack(expand=True)
rightFrame.rowconfigure(0, weight=1)
rightFrame.columnconfigure(0, weight=1)

rightFrame.grid(row=0, column=0, rowspan=2, columnspan=2)
leftTopFrame.grid(row=0, column=2)
leftBottomFrame.grid(row=1, column=2)

f = Figure(figsize=(figSizeX, figSizeY), dpi=100) #figsize sets the area for the graph to appear
a = f.add_subplot(111)

#random values to show a concept
x = [0, 2, 3, 4, 5, 6, 7, 8] 
y = [2, 4, 5, 6, 7, 5, 3, 5] 
t = [1, 2, 3, 4, 5, 6, 7, 8] 

#plots the lines based on above values
a.plot(t, x, label="x-plots") 
a.plot(t, y, label="y-plots") 
a.legend()

#sets up a canvas to draw a graph on and then draws the graph 
canvas = FigureCanvasTkAgg(f, master=leftTopFrame)
canvas.draw()
canvas.get_tk_widget().pack()

# main loop keeps the application open.
root.mainloop()
