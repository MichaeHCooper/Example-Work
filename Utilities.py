"""
Stripped Utilities for Demo

Created - 03.04.2018
Author  - Michael Cooper
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt

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

class DataPlot():
    """
    Class containing functions to plot the various bits and bobs usefull for
    testing.
    """    
    def plotbox(dims, vecs, graph=0, colour='g', scale=1.0,):
        """
        Plots a given box given the pixel dimension. The graph number may
        be specified, hence multiple graphs may be used.
        """
        plt.plot([vecs[5][0]*scale,vecs[6][0]*scale,
                     vecs[7][0]*scale,vecs[8][0]*scale,
                     vecs[5][0]*scale],
                    [vecs[5][1]*scale,vecs[6][1]*scale,
                     vecs[7][1]*scale,vecs[8][1]*scale,
                     vecs[5][1]*scale],'grey',linewidth=1.5)

###############################################################################