"""
Program to plot data in a way simmilar to the matplotlib file.  Created
as matplotlib can't be used on mobiles.

Created on  the 22nd of Jan 2017.

Author, Michael Cooper.
"""

import Image

class graph():

    def __init__(self, imsize=(500,500)):
        """
        Initiates the class and constructs the blank matrix for the
        plot.  White space is represented by 0, axis by 1, grids by 2,
        and finally lines by 3,4,5,6 ect...
        """
        self.xpix = imsize[0]
        self.ypix = imsize[1]
        ypixcount = 0
        self.immat = []
        while ypixcount < self.ypix:
            xpixcount = 0
            immatrow = []
            while xpixcount < self.xpix:
                immatrow.append(0)
                xpixcount = xpixcount+1
            ypixcount = ypixcount+1
            self.immat.append(immatrow)
        self.plinecount=0 #keeps track of the number of plines plotted
        self.plinecol=[] #keeps track of which colour is for each line

    def corners(self, bottomleft=(-5,-5), topright=(5,5)):
        """
        Defines the bottomleft and topright corners of the graph,
        which is then used to scale appropriately the data.
        """
        self.corner0 = (float(bottomleft[0]),float(bottomleft[1]))
        self.corner1 = (float(topright[0]),float(topright[1]))
        self.xfac = self.xpix/(self.corner1[0]-self.corner0[0])
        self.yfac = self.ypix/(self.corner1[1]-self.corner0[1])

    def axis(self): #add pips
        """
        Adds axis to the graph. Optional extra is to ad pips to the
        axis at specified intervalls using a tuple.
        """
        xpixcent = int(round(self.xfac*(-self.corner0[0])))-1
        ypixcent = int(round(self.yfac*(-self.corner0[1])))-1
        if (xpixcent > 0) and (xpixcent < self.xpix):
            for i in self.immat:
                i[xpixcent] = 1
        itercount = 0
        if (ypixcent > 0) and (ypixcent < self.ypix):
            for i in self.immat[ypixcent]:
                self.immat[ypixcent][itercount] = 1
                itercount = itercount+1

    def grid(self, spacing):
        """
        Accepts a tuple which defines the spacing of a background grid
        which is then plotted on the image matrix.
        """
        'null'

    def pline(self, data, linecolour):
        """
        Plots the pline data onto the image matrix by interpolating
        between points.  Line colour is specified as a tuple of three
        values of rgb.
        """
        plinecount = self.plinecount+3
        self.plinecol.append(linecolour)
        itercount = 0
        datalength = len(data)
        while itercount < (datalength-1):
            dx = data[itercount+1][0]-data[itercount][0]
            dy = data[itercount+1][1]-data[itercount][1]
            numx = abs(int(round(dx*self.xfac*2)))
            numy = abs(int(round(dy*self.yfac*2)))
            x = data[itercount][0]
            y = data[itercount][1]
            plotcount = 0
            if numx > numy:
                divx = dx/float(numx)
                divy = dy/float(numx)
                while plotcount <=  numx:
                    intx = int(round(self.xfac*(x-self.corner0[0])))-1
                    inty = int(round(self.yfac*(y-self.corner0[1])))-1
                    if ((intx < self.xpix-1) and (inty < self.ypix-1)
                    	   and (intx > 0) and (inty > 0)):
                        self.immat[inty][intx]=plinecount
                    x = x+divx
                    y = y+divy
                    plotcount = plotcount+1
            else:
                divx=dx/float(numy)
                divy=dy/float(numy)
                while plotcount <=  numy:
                    intx = int(round(self.xfac*(x-self.corner0[0])))-1
                    inty = int(round(self.yfac*(y-self.corner0[1])))-1
                    if ((intx < self.xpix-1) and (inty < self.ypix-1)
                        and (intx > 1) and (inty >1)):
                        self.immat[inty][intx]=plinecount
                    x = x+divx
                    y = y+divy
                    plotcount = plotcount+1
            itercount=itercount+1
            self.plinecount = self.plinecount+1

    def  plot(self, fileloc):
        """
        Plots the image matrix as a picture and saves to file.
        """
        implot = Image.new('RGB', (self.xpix,self.ypix), 'white')
        imfinal = []
        for i in reversed(self.immat):
            for j in i:
                if j == 0:
                    imfinal.append((255,255,255))
                if j == 1:
                    imfinal.append((0,0,0))
                if j == 2:
                    imfinal.append((125,125,125))
                if j >= 3:
                    col = (0,0,0)
                    imfinal.append(col)
        implot.putdata(imfinal)
        implot.save(fileloc)