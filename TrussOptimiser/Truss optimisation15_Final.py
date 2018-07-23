"""
Program to optomise a 2d truss for a specific design brief.
Created on 4th of October 2016.
Author, Michael Cooper.
"""

import matplotlib.pyplot as plt
import random as r
import copy
import time

###############################################################################
###############################################################################

class trussoutput:
    """
    class invollving all of the functions which handle output of truss data.
    """
    def plot(truss, zeroforce='show'):
        """
        Takes a truss file and outputs the nodes and members in a pyplt plot.
        the second argument can either 'show', 'hide' or 'paint, the members
        with zero force.
        """
        pointlistx = []
        pointlisty = []
        for i in truss['node']:
            pointlistx.append(truss['node'][i][0])
            pointlisty.append(truss['node'][i][1])
        plt.plot(pointlistx, pointlisty, 'ro')
        plt.axis([-0.3,0.3,-0.1,0.3])
        for i in truss['member']:
            memberforce = truss['member'][i][5]
            if ((memberforce < 0.001) and (memberforce > -0.001) and
            (zeroforce == 'hide')):
                'null'
            else:
                vx1=truss['node'][truss['member'][i][0]][0]
                vy1=truss['node'][truss['member'][i][0]][1]
                vx2=truss['node'][truss['member'][i][1]][0]
                vy2=truss['node'][truss['member'][i][1]][1]
                if ((memberforce < 0.001) and (memberforce > -0.001) and
                (zeroforce == 'paint')):
                    plt.plot([vx1,vx2], [vy1,vy2], 'c-', lw=2)
                else:
                    plt.plot([vx1,vx2], [vy1,vy2], 'k-', lw=1)
        plt.plot([-0.3,0.3], [0.07,0.07], 'y', lw=1, ls='-.')
        plt.plot([-0.3,0.3], [0.0,0.0], 'y', lw=1, ls='-.')

    def output(truss):
        """
        Takes the truss file and outputs it in a usefull and readable output
        for cross checking by hand.
        """
        text = 'Nodes'+'\n'
        for i in truss['node']:
            text = (text+str(i)+': '+str(truss['node'][i][0])+', '
            +str(truss['node'][i][1])+'\n')
        text = text+'\n'+'Member'+'\n'
        for i in truss['member']:
            text = (text+str(i)+': '+str(truss['member'][i][0])+', '
            +str(truss['member'][i][1])+'   Force(N): '
            +str(round(truss['member'][i][5],3))
            +'   Width(mm): '
            +str(round(((truss['member'][i][6])*1000),3))+'\n')
        return text

###############################################################################
###############################################################################

class truss:
    """
    class that generates a functioning truss from a set of initial points.
    CURRENTLY RECIEVES FULL SET OF NODES AND MEMBERS.
    """
    def __init__(self, truss):
        self.truss = truss

    def memlength(self):
        """
        Calculates the absolute angle of all members at all nodes and adds this
        to the node information.
        """
        for i in self.truss['member']:
            if i[0] == 'm':
                x1=self.truss['node'][self.truss['member'][i][0]][0]
                x2=self.truss['node'][self.truss['member'][i][1]][0]
                y1=self.truss['node'][self.truss['member'][i][0]][1]
                y2=self.truss['node'][self.truss['member'][i][1]][1]
                dx = x1-x2
                dy = y1-y2
                self.truss['member'][i].extend([dx, dy,
                ((dx**2)+(dy**2))**0.5,'f'])

    def memforce(self):
        """
        Calculates the force in each truss member and writes this to the node
        information.
        """
        fcount = 1
        while fcount > 0:
            fcount = 0
            for i in self.truss['node']:
                if i[0] == 'n':
                    unknownfcount = 0
                    unknownlist = []
                    knownlist = []
                    for j in self.truss['member']:
                        if ((self.truss['member'][j][0] == i) or
                        (self.truss['member'][j][1] == i)):
                            if  self.truss['member'][j][5] == 'f':
                                unknownlist.append(j)
                                unknownfcount = unknownfcount+1
                            else:
                                knownlist.append(j)
                    if unknownfcount == 2:
                        mx = 0
                        my = 0
                        for k in knownlist:
                            vecnx = self.truss['member'][k][2]
                            vecny = self.truss['member'][k][3]
                            vecnmod = self.truss['member'][k][4]
                            fn = self.truss['member'][k][5]
                            if self.truss['member'][k][0] == i:
                                mx = mx -(vecnx/vecnmod)*fn
                                my = my -(vecny/vecnmod)*fn
                            if self.truss['member'][k][1] == i:
                                mx = mx +(vecnx/vecnmod)*fn
                                my = my +(vecny/vecnmod)*fn
                        veca = unknownlist[0]
                        vecb = unknownlist[1]
                        if self.truss['member'][veca][0] == i:
                            vecax = -self.truss['member'][veca][2]
                            vecay = -self.truss['member'][veca][3]
                        if self.truss['member'][veca][1] == i:
                            vecax = self.truss['member'][veca][2]
                            vecay = self.truss['member'][veca][3]
                        if self.truss['member'][vecb][0] == i:
                            vecbx = -self.truss['member'][vecb][2]
                            vecby = -self.truss['member'][vecb][3]
                        if self.truss['member'][vecb][1] == i:
                            vecbx = self.truss['member'][vecb][2]
                            vecby = self.truss['member'][vecb][3]
                        vecamod = self.truss['member'][veca][4]
                        vecbmod = self.truss['member'][vecb][4]
                        invdet = (vecamod*vecbmod)/(vecax*vecby-vecay*vecbx)
                        fa = invdet*((vecbx*my)/vecbmod-(vecby*mx)/vecbmod)
                        fb = invdet*((vecay*mx)/vecamod-(vecax*my)/vecamod)
                        self.truss['member'][veca][5]= fa
                        self.truss['member'][vecb][5]= fb
                    if unknownfcount == 1:
                        mx = 0
                        my = 0
                        iterylist = iter(knownlist)
                        next(iterylist)
                        for k in iterylist:
                            vecnx = self.truss['member'][k][2]
                            vecny = self.truss['member'][k][3]
                            vecnmod = self.truss['member'][k][4]
                            fn = self.truss['member'][k][5]
                            if self.truss['member'][k][0] == i:
                                mx = mx -(vecnx/vecnmod)*fn
                                my = my -(vecny/vecnmod)*fn
                            if self.truss['member'][k][1] == i:
                                mx = mx +(vecnx/vecnmod)*fn
                                my = my +(vecny/vecnmod)*fn
                        veca = unknownlist[0]
                        vecb = knownlist[0]
                        if self.truss['member'][veca][0] == i:
                            vecax = -self.truss['member'][veca][2]
                            vecay = -self.truss['member'][veca][3]
                        if self.truss['member'][veca][1] == i:
                            vecax = self.truss['member'][veca][2]
                            vecay = self.truss['member'][veca][3]
                        if self.truss['member'][vecb][0] == i:
                            vecbx = -self.truss['member'][vecb][2]
                            vecby = -self.truss['member'][vecb][3]
                        if self.truss['member'][vecb][1] == i:
                            vecbx = self.truss['member'][vecb][2]
                            vecby = self.truss['member'][vecb][3]
                        vecamod = self.truss['member'][veca][4]
                        vecbmod = self.truss['member'][vecb][4]
                        invdet = (vecamod*vecbmod)/(vecax*vecby-vecay*vecbx)
                        fa = invdet*((vecbx*my)/vecbmod-(vecby*mx)/vecbmod)
                        self.truss['member'][veca][5]= fa
            for j in self.truss['member']:
                if self.truss['member'][j][5] == 'f':
                    fcount = fcount+1

    def memwidth(self):
        """
        Calculates the minimum required width of each member and appends this
        to each member info.
        """
        area = 0
        for i in self.truss['member']:
            memlength = self.truss['member'][i][4]
            memforce = self.truss['member'][i][5]
            if memforce < 0:
                a = -memforce
                b = memlength
                x = 0.01
                xdif = 1
                while xdif > 0.00001:
                    f = ((2.1201e12*x**3)-(1.7668e7*a*x**2)-(1.2e5*a*b**2))
                    fprime = ((6.3603e12*x**2)-(3.5336e7*a*x))
                    fprime2 = ((1.2721e13*x)-(3.5336e7*a))
                    xn = x-((2*f*fprime)/((2*fprime**2)-(f*fprime2)))
                    xdif = abs(xn-x)
                    x=xn
                w=x
            else:
                w = memforce/120000
            self.truss['member'][i].append(w)
            area = area+w*memlength
        return area

###############################################################################
###############################################################################

class trussinit:
    """
    Used to generate an initial truss file with node locations and member
    links. Can generate a number of predefined truss types which then have
    their geometries optimised.
    """
    def seedgeom(trusstype, cellno):
        """
        Generates the geom. The trusstypes are; 'warren', 'pratt', 'howwe',
        'invpratt', 'invhowwe', 'k' and 'invk'. The number of cells determines
        how many divisions are in the truss in either half.
        """
        ######################### Initial Generation ##########################

        geom = {'node':{'nC0':[0.000,0.050],
                        'nL0':[-0.250,0.000],
                        'nR0':[0.250,0.000],
                        'rC0':[0.000,0.070],
                        'rL0':[-0.250,-0.020],
                        'rR0':[0.250,-0.020]},
                'member':{'sCT0':['nC0','rC0',0.0,-0.02,0.02,-390], #!!!!!!!!!!! program in FOS
                          'sLB0':['nL0','rL0',0.0,0.02,0.02,-195],  #!!!!!!!!!!! program in FOS
                          'sRB0':['nR0','rR0',0.0,0.02,0.02,-195]}} #!!!!!!!!!!! program in FOS

        ########################### Node Generation ###########################

        if ((trusstype == 'pratt') or (trusstype == 'howwe') or
        (trusstype == 'invpratt') or (trusstype == 'invhowwe')):
            geom['node']['nC1'] = [0.000,0.000]
            xdist = 0.250/cellno
            nodecount = 1
            xrolldist = xdist
            while nodecount < cellno:
                geom['node']['nL'+str(2*nodecount)] = [xrolldist-0.250,0.000]
                geom['node']['nR'+str(2*nodecount)] = [0.250-xrolldist,0.000]
                geom['node']['nL'+str(2*nodecount-1)] = [xrolldist-0.250,0.050]
                geom['node']['nR'+str(2*nodecount-1)] = [0.250-xrolldist,0.050]
                nodecount = nodecount+1
                xrolldist = xrolldist+xdist

        if trusstype == 'warren':
            xdist = 0.5/(2*cellno-1)
            nodecount = 1
            xrolldist = xdist
            while nodecount < cellno:
                geom['node']['nL'+str(2*nodecount)] = [xrolldist-0.250,0.000]
                geom['node']['nR'+str(2*nodecount)] = [0.250-xrolldist,0.000]
                geom['node']['nL'+str(2*nodecount-1)] = [(xrolldist-0.250-
                (xdist/2)),0.050]
                geom['node']['nR'+str(2*nodecount-1)] = [(0.250+(xdist/2)-
                xrolldist),0.050]
                nodecount = nodecount+1
                xrolldist = xrolldist+xdist

        ######################### Member Generation ##########################

        if ((trusstype == 'pratt') or (trusstype == 'howwe') or
        (trusstype == 'invpratt') or (trusstype == 'invhowwe')):
            if cellno > 1:
                geom['member']['mCC0']=['nC0','nC1']
                geom['member']['mLD0']=['nL0','nL1']
                geom['member']['mRD0']=['nR0','nR1']
                geom['member']['mLB0']=['nL0','nL2']
                geom['member']['mRB0']=['nR0','nR2']
            else:
                geom['member']['mCC0']=['nC0','nC1']
                geom['member']['mLD0']=['nL0','nC0']
                geom['member']['mRD0']=['nR0','nC0']
                geom['member']['mLB0']=['nL0','nC1']
                geom['member']['mRB0']=['nR0','nC1']
            nodecount = 1
            while nodecount < (cellno-1):
                geom['member']['mLC'+str(nodecount)]=['nL'+str(nodecount*2),
                'nL'+str(nodecount*2-1)]
                geom['member']['mRC'+str(nodecount)]=['nR'+str(nodecount*2),
                'nR'+str(nodecount*2-1)]
                geom['member']['mLT'+str(nodecount)]=['nL'+str(nodecount*2-1),
                'nL'+str(nodecount*2+1)]
                geom['member']['mRT'+str(nodecount)]=['nR'+str(nodecount*2-1),
                'nR'+str(nodecount*2+1)]
                geom['member']['mLB'+str(nodecount)]=['nL'+str(nodecount*2),
                'nL'+str(nodecount*2+2)]
                geom['member']['mRB'+str(nodecount)]=['nR'+str(nodecount*2),
                'nR'+str(nodecount*2+2)]
                nodecount = nodecount+1
            if cellno > 1:
                geom['member']['mLC'+str(nodecount)]=['nL'+str(nodecount*2),
                'nL'+str(nodecount*2-1)]
                geom['member']['mRC'+str(nodecount)]=['nR'+str(nodecount*2),
                'nR'+str(nodecount*2-1)]
                geom['member']['mLT'+str(nodecount)]=['nL'+str(nodecount*2-1),
                'nC0']
                geom['member']['mRT'+str(nodecount)]=['nR'+str(nodecount*2-1),
                'nC0']
                geom['member']['mLB'+str(nodecount)]=['nL'+str(nodecount*2),
                'nC1']
                geom['member']['mRB'+str(nodecount)]=['nR'+str(nodecount*2),
                'nC1']

        if trusstype == 'pratt':
            nodecount = 1
            while nodecount < (cellno-1):
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2-1),
                'nL'+str(nodecount*2+2)]
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2-1),
                'nR'+str(nodecount*2+2)]
                nodecount = nodecount+1
            if cellno > 1:
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2-1),
                'nC1']
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2-1),
                'nC1']

        if trusstype == 'howwe':
            nodecount = 1
            while nodecount < (cellno-1):
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2),
                'nL'+str(nodecount*2+1)]
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2),
                'nR'+str(nodecount*2+1)]
                nodecount = nodecount+1
            if cellno > 1:
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2),
                'nC0']
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2),
                'nC0']

        if trusstype == 'invpratt':
            nodecount = 1
            while nodecount < (cellno-1):
                nodemod = 0.5*(-1)**nodecount
                geom['member']['mLD'+str(nodecount)]=[('nL'+
                str(int(nodecount*2-0.5+nodemod))),
                'nL'+str(int(nodecount*2+1.5-nodemod))]
                geom['member']['mRD'+str(nodecount)]=[('nR'+
                str(int(nodecount*2-0.5+nodemod))),
                'nR'+str(int(nodecount*2+1.5-nodemod))]
                nodecount = nodecount+1
            if (cellno > 1) and (nodecount % 2 == 0):
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2),
                'nC0']
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2),
                'nC0']
            if (cellno > 1) and (nodecount % 2 != 0):
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2-1),
                'nC1']
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2-1),
                'nC1']

        if trusstype == 'invhowwe':
            nodecount = 1
            while nodecount < (cellno-1):
                nodemod = -(0.5*(-1)**nodecount)
                geom['member']['mLD'+str(nodecount)]=[('nL'+
                str(int(nodecount*2-0.5+nodemod))),
                'nL'+str(int(nodecount*2+1.5-nodemod))]
                geom['member']['mRD'+str(nodecount)]=[('nR'+
                str(int(nodecount*2-0.5+nodemod))),
                'nR'+str(int(nodecount*2+1.5-nodemod))]
                nodecount = nodecount+1
            if (cellno > 1) and (nodecount % 2 != 0):
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2),
                'nC0']
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2),
                'nC0']
            if (cellno > 1) and (nodecount % 2 == 0):
                geom['member']['mLD'+str(nodecount)]=['nL'+str(nodecount*2-1),
                'nC1']
                geom['member']['mRD'+str(nodecount)]=['nR'+str(nodecount*2-1),
                'nC1']

        if trusstype == 'warren':
            nodecount1 = 0
            while nodecount1 < (cellno-1)*2:
                geom['member']['mLD'+str(nodecount1)]=['nL'+str(nodecount1),
                'nL'+str(nodecount1+1)]
                geom['member']['mRD'+str(nodecount1)]=['nR'+str(nodecount1),
                'nR'+str(nodecount1+1)]
                nodecount1 = nodecount1+1
            nodecount2 = 0
            while nodecount2 < cellno-1:
                geom['member']['mLB'+str(nodecount2)]=['nL'+str(nodecount2*2),
                'nL'+str(nodecount2*2+2)]
                geom['member']['mRB'+str(nodecount2)]=['nR'+str(nodecount2*2),
                'nR'+str(nodecount2*2+2)]
                nodecount2 = nodecount2+1
            nodecount3 = 1
            while nodecount3 < cellno-1:
                geom['member']['mLT'+str(nodecount3)]=[('nL'+
                str(nodecount3*2-1)),'nL'+str(nodecount3*2+1)]
                geom['member']['mRT'+str(nodecount3)]=[('nR'+
                str(nodecount3*2-1)),'nR'+str(nodecount3*2+1)]
                nodecount3 = nodecount3+1
            if (cellno > 1):
                geom['member']['mLT'+str(nodecount3)]=[('nL'
                +str(nodecount3*2-1)),'nC0']
                geom['member']['mRT'+str(nodecount3)]=[('nR'
                +str(nodecount3*2-1)),'nC0']
                geom['member']['mCB0']=['nR'+str(nodecount2*2),
                'nL'+str(nodecount2*2)]
                geom['member']['mLD'+str(nodecount1)]=['nL'+str(nodecount1),
                'nC0']
                geom['member']['mRD'+str(nodecount1)]=['nR'+str(nodecount1),
                'nC0']
            if cellno == 1:
                geom['member']['mCB0']=['nL0','nR0']
                geom['member']['mLD0']=['nL0','nC0']
                geom['member']['mRD0']=['nR0','nC0']

        return geom

###############################################################################
###############################################################################

class trussopt:
    """
    Contains the functions required for genetically optimising trusses.
    """
    def ranmove():
        """
        Has a 20% chance to generate a random number between -0.02 and 0.02.
        Has a 80% chance to be zero.
        This means that most of the time a node will not move, increasing
        effeciency of algorithm. It rounds to 0.1mm for usefulness.
        """
        ran1 = r.random()
        ran2 = r.random()
        if ran1 < 0.9:
            return 0
        else:
            return round((ran2*0.04-0.02),4)

    def flycheck(trussinit, output='mass'):
        """
        Runs all of the steps required to calculate and check a truss on the
        fly, will either output 'mass' or 'truss'
        """
        flytruss = truss(trussinit)
        flytruss.memlength()
        flytruss.memforce()
        flytruss.memwidth()
        if output == 'mass':
            return flytruss.memwidth()
        if output == 'truss':
            flytruss.memwidth()
            return flytruss.truss

    def genopt(seedtruss, numchild):
        """
        Takes a seed truss and optimises it using a genetic optimisation.
        """
        childcount = 0
        parent = copy.deepcopy(seedtruss)
        parentmass = trussopt.flycheck(copy.deepcopy(parent))
        while childcount <= numchild:
            try:
                child = copy.deepcopy(parent) # giving birth
                for i in child['node']: # random variation
                    if (((i[1] == 'L') or (i[1] == 'R')) and (i[2] != '0') and
                    (i[0] != 'r')):
                        ranx = trussopt.ranmove()
                        rany = trussopt.ranmove()
                        nRx = child['node']['nR'+str(i[2])][0] + ranx
                        child['node']['nR'+str(i[2])][0] = nRx
                        nRy = child['node']['nR'+str(i[2])][1] + rany
                        if nRy > 0.07:
                            nRy = 0
                        if nRy < 0.00:
                            nRy = 0
                        else:
                            child['node']['nR'+str(i[2])][1] = nRy
                        nLx = child['node']['nL'+str(i[2])][0] - ranx
                        child['node']['nL'+str(i[2])][0] = nLx
                        nLy = child['node']['nL'+str(i[2])][1] + rany
                        if nLy > 0.07:
                            nLy = 0
                        if nLy < 0.00:
                            nLy = 0
                        else:
                            child['node']['nL'+str(i[2])][1] = nLy
                    if (i[1] == 'C') and (i[0] != 'r'):
                        nCy = child['node'][i][1] + rany
                        if nCy > 0.07:
                            nCy = 0
                        if nCy < 0.00:
                            nCy = 0
                        else:
                            child['node'][i][1] = nCy
                childmass = trussopt.flycheck(copy.deepcopy(child))
                if childmass < parentmass: # surviving
                    parent = copy.deepcopy(child)
                    parentmass = childmass
                    childcount = 0
                    #print('new parent found  ' + str(parentmass)) !!!!!!!!!!!! Delete
                else: # dying
                    childcount = childcount+1
            except:
                childcount = childcount+1
        return trussopt.flycheck(copy.deepcopy(parent), 'truss')
        
    def specopt(trusslist, numcells, increasefunc, timeinterval):
        """
        The final function which iterates through specified truss types and
        for a specified number of cells to find the most optimal truss. The
        program continues to iterate for ever and writes to file every ten
        minutes the best truss. The function can also have the generations
        to be checked through to be increased each time by a
        specified function.
        """
        celllist = []
        numcount = 1
        while numcount <= numcells:
            celllist.append(numcount)
            numcount = numcount+1
        loop = 0
        loopcount = 1
        optimalmass = 1.0
        optimaltrussno = 0
        starttime = time.clock()
        while loop < 1:
            x=loopcount
            y = eval(increasefunc)
            for i in celllist:
                for j in trusslist:
                    try:
                        seed = copy.deepcopy(trussinit.seedgeom(j, i))
                        child = copy.deepcopy(trussopt.genopt(seed, y))
                        childmass = trussopt.flycheck(copy.deepcopy(child))
                        curtime = time.clock()
                        print('Truss Checked')
                        if childmass < optimalmass:
                            optimalmass = childmass
                            optimal = copy.deepcopy(child)
                            optimaltrussno = optimaltrussno+1
                            print('Mass: '+str(optimalmass)+'  NEW OPTIMAL')
                        if curtime > starttime+timeinterval:
                            starttime = curtime
                            file = open(('truss'+str(optimaltrussno)+'-'+
                            time.strftime("%Y_%m_%d_%H_%M_%S")+'-.txt'), 'w')
                            fillcontent= ('Time\n'+
                            time.strftime("%Y_%m_%d_%H_%M_%S")+'\n\nTruss mass\n'+
                            str(optimalmass)+'\n\n'+
                            trussoutput.output(copy.deepcopy(optimal))+
                            '\nActual File\n'+str(optimal))
                            file.write(fillcontent)
                            file.close()
                    except:
                        'null'
            loopcount = loopcount+1
            print(('Loop Count: '+str(loopcount)+'  y: '+str(y)+
            '  NEW LOOP!!!!!'))

###############################################################################
###############################################################################

initfile = open('init.txt', 'r')
initlist = initfile.read().split('\n')
trusslist = initlist[1].split(' ')
numcells = int(initlist[4])
increasefunc = initlist[7]
timeinterval = float(initlist[10])
trussopt.specopt(trusslist, numcells, increasefunc, timeinterval)

###############################################################################
###############################################################################