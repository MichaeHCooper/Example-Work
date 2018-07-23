"""
Program to perform real time analyse the stability of the lambda structure
by allowing variation in leg geometry.
Created on the 27th of Feb 2017.
Author, Michael Cooper.

Notes.
All coordinates are defined in the form [x,y,z]
"""

import numpy as np
import math as m
from tkinter import *

###############################################################################
###############################################################################

class lambdastruc():
    """
    Creates a class based around the lambda structure.
    """
    def __init__(self, dims, weights, tubedia, windpres, cptube):
        """
        Initiates the object from the initial dimensions.
        """
        self.windpres = windpres # Expects a float of wind pressure in Pa 
        self.tubedia = tubedia # Expectes a float of tube dia in m
        self.cptube = cptube
        self.dims = dims # Expected in format [W1, W2, L1, L2, L3]
        self.weights = weights # Tube, Cap, Center, Feet

    def strucgeom(self):
        """
        Takes five variables about the structure and calculates the corodinates
        in xyz space of each of the points of the lambda structure.
        """
        W1 = self.dims[0]
        W2 = self.dims[1]
        L1 = self.dims[2]
        L2 = self.dims[3]
        L3 = self.dims[4]

        P0 = [0.0, 0.0, 0.0] # This is the anchor point, I.E. the first foot.

        W1proj = ((W1**2) - (W2**2)/4)**0.5 # W1 projected in the xz plane.
        L2proj = ((L2**2) - (W2**2)/4)**0.5 # L2 projected in the xz plane.

        P1 = [W1proj, W2/2, 0.0] # Second foot.
        P2 = [W1proj, -W2/2, 0.0] # Third foot.

        P3x = (L1**2 - L2proj**2 + W1proj**2)/(2*W1proj)
        P3z = (L1**2 - P3x**2)**0.5
        P3 = [P3x, 0.0, P3z] # The central node.

        P4x = P3x+((L3**2)/(1+(P3z/P3x)**2))**0.5
        P4z = P3z+((L3**2)/(1+(P3x/P3z)**2))**0.5
        P4 = [P4x, 0.0, P4z] # The end point.

        self.nodes = [P0, P1, P2, P3, P4]

    def masscent(self):
        """
        Claculates the center of mass of the entire structure and total weight.
        """
        L1 = self.dims[2]
        L2 = self.dims[3]
        L3 = self.dims[4]
        tubew = self.weights[0]
        capw  = self.weights[1]
        centw = self.weights[2]
        footw = self.weights[3]
        M1 = L1*tubew
        M2 = L2*tubew
        M3 = L3*tubew
        x1 = (self.nodes[0][0]+self.nodes[3][0])/2
        x2 = (self.nodes[1][0]+self.nodes[3][0])/2
        x3 = (self.nodes[4][0]+self.nodes[3][0])/2
        z1 = (self.nodes[0][2]+self.nodes[3][2])/2
        z2 = (self.nodes[1][2]+self.nodes[3][2])/2
        z3 = (self.nodes[4][2]+self.nodes[3][2])/2

        totalw = M1+M2*2+M3+capw+centw+footw*3
        masscentx = ((M1*x1+M2*x2*2.0+M3*x3+capw*self.nodes[4][0]+
        centw*self.nodes[3][0]+footw*self.nodes[0][0]+
        footw*2*self.nodes[1][0])/totalw)
        masscentz = ((M1*z1+M2*z2*2.0+M3*z3+capw*self.nodes[4][2]+
        centw*self.nodes[3][2]+footw*self.nodes[0][2]+
        footw*2*self.nodes[1][2])/totalw)
        masscenty = 0.0

        self.cmloc = [masscentx, masscenty, masscentz]
        self.totalw = totalw

    def topplesafe(self):
        """
        Calculates the factor of saftey in toppling by taking the smallest
        factor of saftey of toppling about either of the edges.
        """
        leg1projx = self.nodes[3][2]-self.nodes[0][2]
        leg2projx = ((((self.nodes[3][2]-self.nodes[2][2])**2)+
        ((self.nodes[3][1]-self.nodes[2][1])**2))**0.5)
        leg4projx = self.nodes[4][2]-self.nodes[3][2]

        overturnMx = (((leg1projx*(self.nodes[0][2]+self.nodes[3][2])*0.5)
        +(leg2projx*(self.nodes[1][2]+self.nodes[3][2]))
        +(leg4projx*(self.nodes[4][2]+self.nodes[3][2])*0.5))
        *self.tubedia*self.windpres*self.cptube)
        restrainMx = (self.nodes[2][0]-self.cmloc[0])*self.totalw

        safteyx = restrainMx/overturnMx
        
        print(overturnMx)
        print(self.nodes[2][0])

        """
        For the next section the toppling saftey factor is calculated about
        the other edge, the easiest way to do this is to simply rotate the
        nodes so that the edge is now paralel to the y axis.
        """

        theta = m.atan(self.nodes[1][1]/self.nodes[1][0])
        n4 = self.nodes.copy()
        n4.append([self.cmloc[0],self.cmloc[1],self.nodes[3][2]])
        n5 = np.transpose(np.matrix(n4))
        rot = np.matrix([[m.cos(theta),-m.sin(theta),0.0],[m.sin(theta),
                          m.cos(theta),0.0],[0.0,0.0,1.0]])
        nodesrot = np.transpose(rot*n5)

        leg1projrot = ((((float(nodesrot[0,0])-float(nodesrot[3,0]))**2)+
                      ((float(nodesrot[0,2])-float(nodesrot[3,2]))**2))**0.5)
        leg2projrot = ((((float(nodesrot[1,0])-float(nodesrot[3,0]))**2)+
                      ((float(nodesrot[1,2])-float(nodesrot[3,2]))**2))**0.5)
        leg3projrot = ((((float(nodesrot[2,0])-float(nodesrot[3,0]))**2)+
                      ((float(nodesrot[2,2])-float(nodesrot[3,2]))**2))**0.5)
        leg4projrot = ((((float(nodesrot[4,0])-float(nodesrot[3,0]))**2)+
                      ((float(nodesrot[4,2])-float(nodesrot[3,2]))**2))**0.5)
        overturnMrot = (((leg1projrot*(self.nodes[0][2]+self.nodes[3][2])*0.5)+
                         (leg2projrot*(self.nodes[1][2]+self.nodes[3][2])*0.5)+
                         (leg3projrot*(self.nodes[2][2]+self.nodes[3][2])*0.5)+
                         (leg4projrot*(self.nodes[4][2]+self.nodes[3][2])*0.5))
                         *self.tubedia*self.windpres*self.cptube)
        restrainMrot = float(nodesrot[5,1])*self.totalw

        safteyrot = restrainMrot/overturnMrot

        self.topfacx = safteyx
        self.topfacrot = safteyrot
        
        print(overturnMrot)
        print(nodesrot[5,1])

    def reactions(self):
        """
        Calculates the maximum vertical reactions at the feet.
        """
        leg1projz = self.nodes[3][0]-self.nodes[0][0]
        leg2projz = ((((self.nodes[3][0]-self.nodes[2][0])**2)+
        ((self.nodes[3][1]-self.nodes[2][1])**2))**0.5)
        leg4projz = self.nodes[4][0]-self.nodes[3][0]

        windM = (((leg1projz*(self.nodes[0][0]+self.nodes[3][0])*0.5)
        +(leg2projz*(self.nodes[1][0]+self.nodes[3][0]))
        +(leg4projz*(self.nodes[4][0]+self.nodes[3][0])*0.5))
        *self.tubedia*self.windpres*self.cptube)
        windF = ((leg1projz+leg4projz+leg2projz*2)*
                 self.tubedia*self.windpres*self.cptube)

        massM = (self.cmloc[0])*self.totalw
        
        totM = massM#*1.35+windM*1.5
        r2 = totM/(2*self.nodes[1][0])
        totF = self.totalw+windF
        r1 = totF-2*r2
        
        self.r0 = r1
        self.r1 = r2
        self.r2 = r2
    
    def moments(self):
        """
        Calculates the maximum moments about the central node for the three
        supporting legs.
        """
        leg1projz = self.nodes[3][0]-self.nodes[0][0]
        leg2projz = ((((self.nodes[3][0]-self.nodes[2][0])**2)+
        ((self.nodes[3][1]-self.nodes[2][1])**2))**0.5)

        self.M0 = leg1projz*self.r0
        self.M1 = leg2projz*self.r1
        self.M2 = leg2projz*self.r2

###############################################################################
###############################################################################


weights = [12.4, 50, 150, 100]
tubedia = 0.08
windpressure = 227
cptube = 0.5

dimsS5 = [2.7,2.7,3.5,3.5,6]
S5 = lambdastruc(dimsS5, weights, tubedia, windpressure, cptube)
S5.strucgeom()
S5.masscent()
S5.reactions()
S5.topplesafe()

#print(S5.r0)
#print(S5.r1)
#print(S5.r2)

#print('\n',S5.nodes)



###############################################################################
###############################################################################


def update():
    try:
        canv.delete("all")
        safefacx.delete('1.0', END)
        safefacrot.delete('1.0', END)
    
        dims = [w1.get()/1000.0, w2.get()/1000.0, l1.get()/1000.0, l2.get()/1000.0,
                l3.get()/1000.0]
        weights = [float(weight1var.get()), float(weight2var.get()), float(weight3var.get()), float(weight4var.get())]
        tubedia = float(tubedia1var.get())/1000
        windpressure = float(windpres1var.get())*1000
        cptube = float(cptube1var.get())
        forcescale = 4.0e-3
        fly = lambdastruc(dims, weights, tubedia, windpressure, cptube)
        fly.strucgeom()
        fly.masscent()
        fly.topplesafe()
        fly.reactions()
        fly.moments()
        
        if fly.M0 < fly.M1:
            maxM = fly.M0
        else:
            maxM = fly.M1
    
        n1 = []
        for i in fly.nodes:
            x = i[0]
            y = i[1]
            z = i[2]
            n1.append([x-fly.nodes[3][0],y-fly.nodes[3][1],z-fly.nodes[3][2]])
        n1.append([fly.cmloc[0]-fly.nodes[3][0],fly.cmloc[1]-fly.nodes[3][1],
                   fly.cmloc[2]-fly.nodes[3][2]])
        n1.append([fly.cmloc[0]-fly.nodes[3][0],fly.cmloc[1]-fly.nodes[3][1],
                   fly.cmloc[2]-fly.nodes[3][2]-1.0])
        n1.append([n1[0][0],n1[0][1],n1[0][2]+fly.r0*forcescale])
        n1.append([n1[1][0],n1[1][1],n1[1][2]+fly.r1*forcescale])
        n1.append([n1[2][0],n1[2][1],n1[2][2]+fly.r2*forcescale])
        
    
        n2 = np.transpose(np.matrix(n1))
    
        theta1rad = (theta1.get()-180)*m.pi/180
        theta2rad = (theta2.get()-180)*m.pi/180
        zrot = np.matrix([[m.cos(theta1rad),-m.sin(theta1rad),0.0],
                          [m.sin(theta1rad),m.cos(theta1rad),0.0],
                          [0.0,0.0,1.0]])
        xrot = np.matrix([[1.0,0.0,0.0],
                          [0.0,m.cos(theta2rad),-m.sin(theta2rad)],
                          [0.0,m.sin(theta2rad),m.cos(theta2rad)]])
    
        t1 = 50*np.matrix([[1,0,0],[0,1,0],[0,0,-1]])*(xrot*(zrot*n2))
        t2 = np.transpose(np.matrix([[250,250,250,250,250,250,250,250,250,250],[0,0,0,0,0,0,0,0,0,0],
                                     [250,250,250,250,250,250,250,250,250,250]])+t1)
    
        canv.create_line(int(t2[5,0]),int(t2[5,2]),int(t2[6,0]),int(t2[6,2]), width=5, arrow=LAST, fill = 'blue')
        canv.create_oval(int(t2[5,0])-5,int(t2[5,2])-5,int(t2[5,0])+5,int(t2[5,2])+5, fill='lightgrey', outline='blue', width=2)
    
        canv.create_line(int(t2[0,0]),int(t2[0,2]),int(t2[3,0]),int(t2[3,2]), width=5)
        canv.create_line(int(t2[1,0]),int(t2[1,2]),int(t2[3,0]),int(t2[3,2]), width=5)
        canv.create_line(int(t2[2,0]),int(t2[2,2]),int(t2[3,0]),int(t2[3,2]), width=5)
        canv.create_line(int(t2[4,0]),int(t2[4,2]),int(t2[3,0]),int(t2[3,2]), width=5)
        
        w = 5
        canv.create_oval(int(t2[0,0])-w,int(t2[0,2])-w,int(t2[0,0])+w,int(t2[0,2])+w, fill='black')
        canv.create_oval(int(t2[1,0])-w,int(t2[1,2])-w,int(t2[1,0])+w,int(t2[1,2])+w, fill='black')
        canv.create_oval(int(t2[2,0])-w,int(t2[2,2])-w,int(t2[2,0])+w,int(t2[2,2])+w, fill='black')
        canv.create_oval(int(t2[3,0])-w,int(t2[3,2])-w,int(t2[3,0])+w,int(t2[3,2])+w, fill='black')
        canv.create_oval(int(t2[4,0])-w,int(t2[4,2])-w,int(t2[4,0])+w,int(t2[4,2])+w, fill='black')
        
        canv.create_line(int(t2[0,0]),int(t2[0,2]),int(t2[7,0]),int(t2[7,2]), width=5, arrow=LAST, fill = 'red')
        canv.create_line(int(t2[1,0]),int(t2[1,2]),int(t2[8,0]),int(t2[8,2]), width=5, arrow=LAST, fill = 'red')
        canv.create_line(int(t2[2,0]),int(t2[2,2]),int(t2[9,0]),int(t2[9,2]), width=5, arrow=LAST, fill = 'red')
    
        safefacx.insert(END, ('   '+str(round(fly.topfacx, 3))+'  Topling factor of saftey about front edge.'))
        safefacrot.insert(END, ('   '+str(round(fly.topfacrot, 3))+'  Topling factor of saftey about side edge.'))
        maxmoment.insert(END, ('   '+str(round(maxM/1000, 3))+'  Maximum moment transfered between the legs and the center joint, KNm'))
    except:
        'null'
    safefacx.after(10, update)

#------------------------------------------------------------------------------

master = Tk()

#------------------------------------------------------------------------------

w1 = Scale(master, from_=0, to=10000,tickinterval=1000, orient=HORIZONTAL,
           length=650)
w1.set(4000)
w1.grid(row=1, column=1)
w2 = Scale(master, from_=0, to=10000,tickinterval=1000, orient=HORIZONTAL,
           length=650)
w2.set(4000)
w2.grid(row=2, column=1)
l1 = Scale(master, from_=0, to=10000,tickinterval=1000, orient=HORIZONTAL,
           length=650)
l1.set(4000)
l1.grid(row=3, column=1)
l2 = Scale(master, from_=0, to=10000,tickinterval=1000, orient=HORIZONTAL,
           length=650)
l2.set(4000)
l2.grid(row=4, column=1)
l3 = Scale(master, from_=0, to=10000,tickinterval=1000, orient=HORIZONTAL,
           length=650)
l3.set(4000)
l3.grid(row=5, column=1)

#------------------------------------------------------------------------------

canv = Canvas(master, width=500, height=500)
canv.grid(row=6, column=1, rowspan=9)

#------------------------------------------------------------------------------

weight1var = StringVar()
weight1 = Entry(master, width=6, textvariable=weight1var)
weight1var.set('12.4')
weight1.grid(row=1, column=4)

weight2var = StringVar()
weight2 = Entry(master, width=6, textvariable=weight2var)
weight2var.set('50')
weight2.grid(row=2, column=4)

weight3var = StringVar()
weight3 = Entry(master, width=6, textvariable=weight3var)
weight3var.set('150')
weight3.grid(row=3, column=4)

weight4var = StringVar()
weight4 = Entry(master, width=6, textvariable=weight4var)
weight4var.set('100')
weight4.grid(row=4, column=4)

tubedia1var = StringVar()
tubedia1 = Entry(master, width=6, textvariable=tubedia1var)
tubedia1var.set('80')
tubedia1.grid(row=3, column=4)

windpres1var = StringVar()
windpres1 = Entry(master, width=6, textvariable=windpres1var)
windpres1var.set('0.277')
windpres1.grid(row=1, column=7)

cptube1var = StringVar()
cptube1 = Entry(master, width=6, textvariable=cptube1var)
cptube1var.set('0.5')
cptube1.grid(row=2, column=7)

#------------------------------------------------------------------------------

label1 = Label(master, text="Width 1, mm")
label1.grid(row=1, column=2)
label2 = Label(master, text="Width 2, mm")
label2.grid(row=2, column=2)
label3 = Label(master, text="Leg Length 1, mm")
label3.grid(row=3, column=2)
label4 = Label(master, text="Leg Length 2 & 3, mm ")
label4.grid(row=4, column=2)
label5 = Label(master, text="Extension Length, mm")
label5.grid(row=5, column=2)

label6 = Label(master, text="Weight of Struts, Nm^-1")
label6.grid(row=1, column=5)
label7 = Label(master, text="Weight of Cap, N")
label7.grid(row=2, column=5)
label8 = Label(master, text=" Weight of Central Node, N")
label8.grid(row=3, column=5)
label9 = Label(master, text="Weight of Feet, N")
label9.grid(row=4, column=5)
label10 = Label(master, text="Strut Diameter, mm")
label10.grid(row=5, column=5)

label11 = Label(master, text="Wind Pressure, KPa")
label11.grid(row=1, column=8)
label12 = Label(master, text="Strut Coeficient of Presure")
label12.grid(row=2, column=8)

label13 = Label(master, text="Rotate About Z Axis")
label13.grid(row=11, column=7, columnspan=2)
label14 = Label(master, text="Rotate About X Axis")
label14.grid(row=12, column=7, columnspan=2)

label15 = Label(master, text="Lambda Structure Designer", font=("Courier", 30))
label15.grid(row=0, column=1, columnspan=8)

#------------------------------------------------------------------------------

safefacx = Text(master, height=1, width=80)
safefacx.grid(row=7, column=2, columnspan=7)
safefacrot = Text(master, height=1, width=80)
safefacrot.grid(row=8, column=2, columnspan=7)
maxmoment = Text(master, height=1, width=80)
maxmoment.grid(row=9, column=2, columnspan=7)
safefacx.after(10, update)

#------------------------------------------------------------------------------

theta1 = Scale(master, from_=0, to=360,tickinterval=25, orient=HORIZONTAL,
           length=400)
theta1.set(180)
theta1.grid(row=11, column=2, columnspan=5)
theta2 = Scale(master, from_=0, to=360,tickinterval=25, orient=HORIZONTAL,
           length=400)
theta2.set(180)
theta2.grid(row=12, column=2, columnspan=5)

#------------------------------------------------------------------------------

master.grid_columnconfigure(0, minsize=50)
master.grid_columnconfigure(3, minsize=50)
master.grid_columnconfigure(6, minsize=50)
master.grid_columnconfigure(9, minsize=50)
master.grid_rowconfigure(6, minsize=50)
master.grid_rowconfigure(10, minsize=50)
master.grid_rowconfigure(13, minsize=50)

#------------------------------------------------------------------------------

mainloop()
#"""

###############################################################################
###############################################################################