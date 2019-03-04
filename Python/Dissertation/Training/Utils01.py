"""
Program to cereate the required data fo the "Bot The Builder" network based on
the YOLO netwrok.

Created - 03.04.2018
Author  - Michael Cooper
"""

import numpy as np
import random as ran
import math as m
import matplotlib.pyplot as plt
import sys

#ran.seed(42)

class DataGrid():
    def __init__(self, dims, Grid):
        self.z = dims
        # The width and height of the images in terms of pixels.
        self.Grid = Grid
        # The number of boxs along each edge that the image is split into.

    def boxverticies(self,w,h,x,y,t):
        """
        Calculates the verticies of a specific box given the width, height,
        x and y coordinates of the center and the angle of rotation, theta. In
        addition it also calculates which grid unit the box center belongs,
        this is used for the YOLO teqhnique.
        """
        BaseVecs = np.matrix([[-w*0.5, w*0.5, w*0.5,-w*0.5],
                              [-h*0.5,-h*0.5, h*0.5, h*0.5]])
        RotMat = np.matrix([[m.cos(t),-m.sin(t)],
                            [m.sin(t), m.cos(t)]])
        TransMat = np.matrix([[x,x,x,x],
                              [y,y,y,y]])
        RotVecs = RotMat*BaseVecs
        Vecs = RotVecs+TransMat
        veca = [Vecs[0,0],Vecs[1,0]]
        vecb = [Vecs[0,1],Vecs[1,1]]
        vecc = [Vecs[0,2],Vecs[1,2]]
        vecd = [Vecs[0,3],Vecs[1,3]]
        gx = int(x*self.Grid)
        gy = int(y*self.Grid)
        # gx and gy are the respective grid numbers for the YOLO technique.
        return [w,h,x,y,t,veca,vecb,vecc,vecd,gx,gy]

    def isboxinside(self,vecs):
        """
        Checks wheter a box is actually inside the bounding box given the list
        of verticies.
        """
        veclist = [vecs[5][0],vecs[6][0],vecs[7][0],vecs[8][0],vecs[5][0],
                vecs[5][1],vecs[6][1],vecs[7][1],vecs[8][1],vecs[5][1]]
        inside = True
        for i in veclist:
            if i < 0.0:
                inside = False
            if i > 1:
                inside = False
        return inside

    def isinside(self,vecs,point):
        """
        Checks whether a point lies within a box given a list of verticies.
        """
        inside = False
        A = vecs[5]
        B = vecs[6]
        D = vecs[8]
        AB = [B[0]-A[0],B[1]-A[1]]
        AD = [D[0]-A[0],D[1]-A[1]]
        AP = [point[0]-A[0],point[1]-A[1]]
        ABAB = AB[0]**2+AB[1]**2
        ADAD = AD[0]**2+AD[1]**2
        APAB = AB[0]*AP[0]+AB[1]*AP[1]
        APAD = AD[0]*AP[0]+AD[1]*AP[1]
        if (APAB > 0) and (APAD > 0) and (ABAB > APAB) and (ADAD > APAD):
            inside = True
        return inside

    def ccw(self, veca, vecb, vecc):
        """
        Checks if a set of three points are counter clockwise.
        Credit - http://bryceboe.com/2006/10/23/
        line-segment-intersection-algorithm/ - 2018
        """
        return ((vecc[1]-veca[1])*(vecb[0]-veca[0]) >
                (vecb[1]-veca[1])*(vecc[0]-veca[0]))
    
    def intersect(self, linea, lineb):
        """
        Checks if tow vector lines intersect.
        Credit - http://bryceboe.com/2006/10/23/
        line-segment-intersection-algorithm/ - 2018
        """
        return (self.ccw(linea[0],lineb[0],lineb[1]) != self.ccw(linea[1],lineb[0],lineb[1]) and
                self.ccw(linea[0],linea[1],lineb[0]) != self.ccw(linea[0],linea[1],lineb[1]))
    
    def boxintersect(self, boxa, boxb):
        """
        Checks if two boxes intersect.
        """
        vecsa = boxa[5:9]
        vecsa.append(boxa[5])
        vecsb = boxb[5:9]
        vecsb.append(boxb[5])
        intersect = False
        for i in range(4):
            linea = vecsa[i:i+2]
            for j in range(4):
                lineb = vecsb[j:j+2]
                if self.intersect(linea,lineb) == True:
                    intersect = True
        return intersect
            

    def ranbox(self):
        """
        Returns the varibles and verticies of a random box that lies within
        the bounding box.
        """
        inside = False
        while inside == False:
            w = ran.random()*1.5
            h = ran.random()*1.5
            x = ran.random()
            y = ran.random()
            # w,h,x,y are set so that they are likely to be within the bounds.
            t = ran.random()*m.pi*0.5
            # Creates a random theta between 0 an pi/2.
            vecs = self.boxverticies(w,h,x,y,t)
            inside = self.isboxinside(vecs)
            # Rejects the box and tries again unless it is within the bounds.
            if w < 0.05*h or h < 0.05*w:
                inside = False
            # Rejects a box if the aspect ratio is too small
        return vecs

    def pix(self,vecs):
        """
        Creates an array representing the points which lie within the shape,
        in essence the pixels from a drawing.  The points used are the
        midpoints of the pixels.
        """
        PixList = []
        for i in range(self.z):
            SubList = []
            for j in range(self.z):
                x = (j+0.5)/self.z
                y = (i+0.5)/self.z
                inside = self.isinside(vecs,[x,y])
                SubList.append(inside)
            PixList.append(SubList)
        return np.array(PixList)

    def boxsequence(self, num):
        """
        Creates a series of random squares, then takes the associated pixels
        and combines them, sequentially subtracting them from each other.
        """
        valid = False
        while valid == False:

            valid =  True
            pixlist = np.zeros([self.z,self.z], dtype=bool)
            datalist = []
            datalistout = []

            for i in range(num):
                tempvecs = self.ransquare()
                temppixlist = self.pix(tempvecs)
                datalist.append([tempvecs,temppixlist])
                pixlist = np.logical_or(pixlist,temppixlist)
    
            for i in range(num-1):
                # Checks if all squares overlap and that none are enveloped.
                overlap = np.any(np.logical_and(datalist[i][1],
                                                datalist[i+1][1]))
                envelopeda = np.any(np.logical_and(datalist[i][1],
                                    np.logical_not(datalist[i+1][1])))
                envelopedb = np.any(np.logical_and(datalist[i+1][1],
                                    np.logical_not(datalist[i][1])))
                if (overlap==False)or(envelopeda==False)or(envelopedb==False):
                    valid = False
    
            for i in range(num):
                # Checks that there are actually pixels in a square.
                if np.any(pixlist) == False:
                    valid = False

                datalistout.append([datalist[i][0],pixlist])
                pixlist = np.logical_and(pixlist,
                                         np.logical_not(datalist[i][1]))

        for i in range(len(datalistout)):
                # numbers the order of the data.
            repeatcount = 0
            for j in datalistout[i:]:
                if ((datalistout[i][0][9] == j[0][9]) and 
                   (datalistout[i][0][10] == j[0][10])):
                    repeatcount += 1
            datalistout[i].append(repeatcount-1)

        return datalistout

    def boxsequenceV2(self, num):
        """
        Creates a sequence of random boxes, then creates a union of the pixel
        data for each.
        """
        if num == 1:
            boxlist = []
            tempvecs = self.ranbox()
            boxlist.append(tempvecs)
        else:
            valid = False
            while valid == False:
    
                valid = True
                boxlist = []
    
                for i in range(num):
                    tempvecs = self.ranbox()
                    boxlist.append(tempvecs)
                # Creates the list of boxes.
    
                for i in range(num):
                    subvalid = False
                    for j in range(num):
                        if j == i:
                            continue
                        intersect = self.boxintersect(boxlist[i],boxlist[j])
                        if intersect == True:
                            subvalid = True
                    if subvalid == False:
                        valid = False
            #ensures that all boxes intersect, non itersection is useless.

        pixdata = np.zeros([self.z,self.z])
        for i in boxlist:
            pixdata = np.logical_or(pixdata, self.pix(i))
            #Combines the pixeldata into one image

        for i in range(len(boxlist)):
            # numbers the order of the data.
            repeatcount = 0
            for j in boxlist[i:]:
                if ((boxlist[i][9] == j[9]) and 
                   (boxlist[i][10] == j[10])):
                    repeatcount += 1
            boxlist[i].append(repeatcount-1)

        return boxlist, pixdata

    def createdata(self, Z, boxpergrid):
        """
        Creates the x and y matricies required for the YOLO style neural
        network. Z is a list containing the distribution of square sequences
        required, for instance: 5000 with one box, 1000 with two boxes, ect..

        x shape = Zsum, Dims, Dims, 1
        y shape = Zsum, Grid, Grid, 6*SqSeqNum+1                               Change if number of classifications change

        y values will be inputted into the correct place otherwise the output
        will be zeroed everywhere else.
        """
        subcount = 0
        countsteps = 100

        Zsum = sum(Z)
        X = np.zeros([Zsum,self.z,self.z,1])
        Y = np.zeros([Zsum,self.Grid,self.Grid,6*boxpergrid+1])
        count = 0
        print(np.shape(X))
        print(np.shape(Y))
        for i in range(len(Z)):
            for j in range(Z[i]):
                Valid = False
                while Valid == False: # Checks that grids aren't overfiled.
                    Valid = True
                    boxseq, pixdata = self.boxsequenceV2(i+1)
                    y = np.zeros([self.Grid,self.Grid,6*boxpergrid+1])
                    x = pixdata
                    for k in boxseq:
                        ytemp = k[0:5]
                        ytemp.append(1.0)
                        pos   = k[9:11]
                        order = k[11]
                        try:
                            y[pos[0],pos[1],order*6:order*6+6]=ytemp
                            y[pos[0],pos[1],-1]=1.0
                        except:
                            Valid = False
                x = np.reshape(x, [160,160,1])                                   # Change if data size changes
                X[count] = x
                Y[count] = y
                count+=1

                # Shows how many have been completed in the command bar
                subcount +=1
                if subcount == countsteps:
                    percentdone = (count/Zsum)*100
                    sys.stdout.write('\r'+str(count)+
                    '    '+str(round(percentdone))+'%')
                    subcount = 0
        return X, Y

class DataPlot():
    """
    Class containing functions to plot the various bits and bobs usefull for
    testing.
    """    
    def plotbox(dims, vecs, graph=0, colour='g'):
        """
        Plots a given box given the pixel dimension. The graph number may
        be specified, hence multiple graphs may be used.
        """
        plt.figure(graph)
        plt.plot([vecs[5][0],vecs[6][0],vecs[7][0],vecs[8][0],vecs[5][0]],
         [vecs[5][1],vecs[6][1],vecs[7][1],vecs[8][1],vecs[5][1]],colour)
        plt.plot([0,1,1,0,0],
                 [0,0,1,1,0])

    def plotpix(dims, pixList, graph=0):
        """
        Plots a pixlist. The graph number may be specified, hence multiple
        graphs may be used.
        """
        for i in range(dims):
            for j in range(dims):
                x = (j+0.5)/dims
                y = (i+0.5)/dims
                if pixList[i][j] == True:
                    plt.figure(graph)
                    plt.plot(x,y,'bs')
        plt.plot([0,1,1,0,0],
                 [0,0,1,1,0],'g')

    def plotgrid(Grid, graph=0):
        """
        Plots the gridlines on.
        """
        for i in range(Grid-1):
            plt.figure(graph)
            plt.plot([(i+1)/Grid,(i+1)/Grid],[0,1],'g')
            plt.plot([0,1],[(i+1)/Grid,(i+1)/Grid],'g')

def savedata(X,Y, Xfilename='X', Yfilename='Y'):
    np.save(Xfilename,X)
    np.save(Yfilename,Y)

###############################################################################

"""
Writing Data   !!!! Hash out before using elsewhere !!!!
"""

#Z = [5000,5000,5000,5000]
#
#Data = DataGrid(160,5)
#X,Y = Data.createdata(Z,2)
#savedata(X,Y, 'X20K-5', 'Y20K-5')

Data = DataGrid(160,5)

boxlist,pixlist = Data.boxsequenceV2(3)

DataPlot.plotpix(160,pixlist)