"""
Demonstration software for BTBnet

Author - Michael Cooper
Started - 07.06.18
"""


from tkinter import *
from PIL import ImageGrab, Image, ImageTk
import PIL
import numpy as np
import PictureTester

###############################################################################

BTB = PictureTester.LoadModel('BTBFinal.hdf5')

###############################################################################

def paint(event):
    lwidth = widthslide.get()
    x1, y1 = (event.x - lwidth), (event.y - lwidth)
    x2, y2 = (event.x + lwidth), (event.y + lwidth)
    canv.create_rectangle(x1, y1, x2, y2, fill = 'black', width=0)

def erasor(event):
    lwidth = widthslide.get()
    x1, y1 = (event.x - lwidth), (event.y - lwidth)
    x2, y2 = (event.x + lwidth), (event.y + lwidth)
    canv.create_rectangle(x1, y1, x2, y2, fill = 'white', width=0)

linecoords = []
funcflip = 0

def line(event):
    lwidth = widthslide.get()
    global funcflip
    global linecoords
    if funcflip == 0:
        linecoords.append(event)
        funcflip = 1
    elif funcflip == 1:
        linecoords.append(event)
        x1, y1 = linecoords[0].x, linecoords[0].y
        x2, y2 = linecoords[1].x, linecoords[1].y
        canv.create_line(x1,y1,x2,y2, width=lwidth*2)
        linecoords=[]
        funcflip = 0

###############################################################################

master = Tk()
canv = Canvas(master, width=800, height=800, bg='white')
canv.grid(row=1, column=0, columnspan=5)

def drawpaint():
    canv.bind("<B1-Motion>", paint)
    canv.bind("<Button-1>", paint)
def linepaint():
    canv.bind("<B1-Motion>", 'null')
    canv.bind("<Button-1>", line)
def erasorpaint():
    canv.bind("<B1-Motion>", erasor)
    canv.bind("<Button-1>", erasor)

paintbutton = Button(master, text='Paint', command=drawpaint)
paintbutton.grid(row=0, column=0)
linebutton = Button(master, text='Line', command=linepaint)
linebutton.grid(row=0, column=1)
erasorbutton = Button(master, text='Erasor', command=erasorpaint)
erasorbutton.grid(row=0, column=2)

drawpaint()

widthslide = Scale(master, from_=0, to=100, orient=HORIZONTAL,
           length=300)
widthslide.set(10)
widthslide.grid(row=0, column=3)

###############################################################################

def Solve():
    x=master.winfo_rootx()+canv.winfo_x()
    y=master.winfo_rooty()+canv.winfo_y()
    x1=x+canv.winfo_width()
    y1=y+canv.winfo_height()
    im = ImageGrab.grab().crop((x+2,y+2,x1-2,y1-2))
    im = im.resize((160,160))
    imarray = np.array(im)
    imarray = imarray[:,:,0]
    trutharray = np.zeros((160,160))
    imarray = np.logical_not(np.not_equal(imarray,trutharray))
    imarray = imarray.astype(int)
    PictureTester.test(imarray, BTB, confslide.get()/100.0)

    toshow = Image.open("temp.png")
    toshow = toshow.resize((800,800))
    toshow = ImageTk.PhotoImage(toshow)
    labelim.configure(image=toshow)
    labelim.image=toshow

toshow = Image.open("temp.png")
toshow = toshow.resize((800,800))
toshow = ImageTk.PhotoImage(toshow)
labelim = Label(master, image=toshow)
labelim.image=toshow
labelim.grid(row=1, column=5, columnspan=2)

savebutton = Button(master, text='Save', command=Solve)
savebutton.grid(row=0, column=5)

def resetcanv():
    canv.delete("all")

resetbutton = Button(master, text='Clear', command=resetcanv)
resetbutton.grid(row=0, column=4)

confslide = Scale(master, from_=0, to=100, orient=HORIZONTAL,
           length=300)
confslide.set(31)
confslide.grid(row=0, column=6)

###############################################################################

mainloop()
