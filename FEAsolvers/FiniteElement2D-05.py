"""
2D finite element analysis software using triangular elements.
Started on Dec 4th 2016.
Aurthor: Michael Cooper.
"""

###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import Geomgen

###############################################################################

class solver:
    """
    Creates the solver for the finite element software. It takes in a geometry
    file which exists in a pre-specified manner and spits out an answer.
    """
    def __init__(self, geom):
        """
        Initiates the class.
        """
        self.geom = geom

        """
        Calculates the elasticity matrix, assumes material is unform and
        homogenous, as this variable is used constently but only needs to be
        calculated once.
        """
        E = geom['props']['E']
        v = geom['props']['v']     
        scalar = E/(1-v**2)
        mat = np.matrix([[1,v,0],[v,1,0],[0,0,(1-v)/2]])
        self.elastmat = scalar*mat
        
        """
        Creates the initial golbal matrix.
        """
        dim = len(geom['nodes'])*2
        self.globalmat = np.matrix(np.zeros((dim,dim)))
        self.forcemat = np.matrix(np.zeros((dim,1)))
        self.dispmat = np.matrix(np.zeros((dim,1)))
        for i in self.geom['forces']:
            if self.geom['forces'][i][0] != 'un':
                self.forcemat[(2*int(i[1:])),0] = self.geom['forces'][i][0]
                self.forcemat[(2*int(i[1:])+1),0] = self.geom['forces'][i][1]
        self.refmatglob = np.arange(dim).reshape(dim,1)

    def elarea(self, triname):
        """
        Calculates the area of a given element in the geom file.
        """
        nodea = self.geom['tris'][triname][0]
        nodeb = self.geom['tris'][triname][1]
        nodec = self.geom['tris'][triname][2]
        xa = self.geom['nodes'][nodea][0]
        ya = self.geom['nodes'][nodea][1]
        xb = self.geom['nodes'][nodeb][0]
        yb = self.geom['nodes'][nodeb][1]
        xc = self.geom['nodes'][nodec][0]
        yc = self.geom['nodes'][nodec][1]
        return 0.5*abs((xa-xc)*(yb-ya)-(xa-xb)*(yc-ya))

    def strainmat(self, triname):
        """
        Calculates the strain matrix of a given element in the geom file.
        """
        nodea = self.geom['tris'][triname][0]
        nodeb = self.geom['tris'][triname][1]
        nodec = self.geom['tris'][triname][2]
        xa = self.geom['nodes'][nodea][0]
        ya = self.geom['nodes'][nodea][1]
        xb = self.geom['nodes'][nodeb][0]
        yb = self.geom['nodes'][nodeb][1]
        xc = self.geom['nodes'][nodec][0]
        yc = self.geom['nodes'][nodec][1]
        scalar = 1/(2*self.elarea(triname))
        mat = np.matrix([[(yb-yc),   0   ,(yc-ya),   0   ,(ya-yb),   0   ],
                         [   0   ,(xc-xb),   0   ,(xa-xc),   0   ,(xb-xa)],
                         [(xc-xb),(yb-yc),(xa-xc),(yc-ya),(xb-xa),(ya-yb)]])
        return scalar*mat

    def stiffmat(self, triname):
        """
        Calculates the stiffness matrix of a given elemnt in the geom file.
        """
        D = self.elastmat
        B = self.strainmat(triname)
        delta = self.elarea(triname)
        t = self.geom['props']['t']
        nodea = 2*int(self.geom['tris'][triname][0][1:])
        nodeb = 2*int(self.geom['tris'][triname][1][1:])
        nodec = 2*int(self.geom['tris'][triname][2][1:])
        refmatx = [nodea,nodea+1,nodeb,nodeb+1,nodec,nodec+1]   
        refmaty = refmatx
        K = t*delta*B.T*D*B
        icount = 0
        Kref = []
        for i in refmatx:
            jcount = 0
            for j in refmaty:
                Kref.append([i,j,K[icount,jcount]])
                jcount = jcount+1
            icount = icount+1
        return Kref

    def assembly(self):
        """
        Assembles the global stiffness matrix with the info from each element.
        """
        for i in self.geom['tris']:
            Kref = self.stiffmat(i)
            for j in Kref:
                self.globalmat[j[0],j[1]] = self.globalmat[j[0],j[1]]+j[2]

    def displacements(self):
        """
        Calculates the displacements of each node.
        """
        rowtodel = []
        for i in self.geom['forces']:
            if self.geom['forces'][i][0] == 'un':
                rowtodel.append(2*int(i[1:]))
                rowtodel.append(2*int(i[1:])+1)
        reducedmat = np.delete(self.globalmat, rowtodel, 0)
        reducedmat = np.delete(reducedmat, rowtodel, 1)
        reducedforcemat = np.delete(self.forcemat, rowtodel, 0)
        reduceddispmat = reducedmat.I*reducedforcemat
        reducedrefmat = np.delete(self.refmatglob, rowtodel, 0)
        icount = 0
        for i in np.nditer(reduceddispmat):
            self.dispmat[reducedrefmat[icount],0] = i
            icount = icount+1

    def forces(self):
        """
        Calculats the full set of forces in the plate.
        """
        self.forcemat = self.globalmat*self.dispmat

    def stress(self, triname):
        """
        Calculates the stress state within a triangular element.
        """
        nodea = 2*int(self.geom['tris'][triname][0][1:])
        nodeb = 2*int(self.geom['tris'][triname][1][1:])
        nodec = 2*int(self.geom['tris'][triname][2][1:])
        reduceddispmat = self.dispmat[[nodea,nodea+1,nodeb,nodeb+1,nodec,
                                       nodec+1],0]
        D = self.elastmat
        B = self.strainmat(triname)
        stress = D*B*reduceddispmat
        return stress

    def solve(self):
        """
        Technically the output function but for simplicity for the user it is
        called by 'solve' as this is essntially the overarching function.
        """
        self.assembly()
        self.displacements()
        self.forces()
        output = {'nodes':{},'tris':{}}
        for i in self.geom['nodes']:
            coords = [self.geom['nodes'][i][0],self.geom['nodes'][i][1]]
            xref = 2*int(i[1:])
            yref = 2*int(i[1:])+1
            disps = [self.dispmat[xref, 0], self.dispmat[yref, 0]]
            forces = [self.forcemat[xref, 0], self.forcemat[yref, 0]]
            output['nodes'][i] = [coords, disps, forces]
        for j in self.geom['tris']:
            nodea = self.geom['tris'][j][0]
            nodeb = self.geom['tris'][j][1]
            nodec = self.geom['tris'][j][2]
            nodelist = [nodea,nodeb,nodec]
            stressmat = self.stress(j)
            stresslist = [stressmat[0,0],stressmat[1,0],stressmat[2,0]]
            output['tris'][j] = [nodelist,stresslist]
        return output

###############################################################################

class output:
    """
    Creates the class which handles the post processing of the solver.
    """
    def plot(output, dispscale, axisscale):
        """
        Outputs all of the data into a nice little graph!!!
        """
        plt.axes()
        plt.axis(axisscale)
        for i in output['tris']:
            nodea = output['tris'][i][0][0]
            nodeb = output['tris'][i][0][1]
            nodec = output['tris'][i][0][2]
            xa = output['nodes'][nodea][0][0]
            ya = output['nodes'][nodea][0][1]
            xb = output['nodes'][nodeb][0][0]
            yb = output['nodes'][nodeb][0][1]
            xc = output['nodes'][nodec][0][0]
            yc = output['nodes'][nodec][0][1]
            nodelist = [[xa,ya],[xb,yb],[xc,yc]]
            tri = plt.Polygon(nodelist, fill=None, ls='-')
            plt.gca().add_patch(tri)
            deltaxa = (output['nodes'][nodea][0][0]+
            output['nodes'][nodea][1][0]*dispscale)
            deltaya = (output['nodes'][nodea][0][1]+
            output['nodes'][nodea][1][1]*dispscale)
            deltaxb = (output['nodes'][nodeb][0][0]+
            output['nodes'][nodeb][1][0]*dispscale)
            deltayb = (output['nodes'][nodeb][0][1]+
            output['nodes'][nodeb][1][1]*dispscale)
            deltaxc = (output['nodes'][nodec][0][0]+
            output['nodes'][nodec][1][0]*dispscale)
            deltayc = (output['nodes'][nodec][0][1]+
            output['nodes'][nodec][1][1]*dispscale)
            nodelist = [[deltaxa,deltaya],[deltaxb,deltayb],[deltaxc,deltayc]]
            deltatri = plt.Polygon(nodelist, fill=None, ls='--')
            plt.gca().add_patch(deltatri)
    plt.show()

###############################################################################

plate1 = solver(Geomgen.beam('n47'))

solution = plate1.solve()

output.plot(solution, 1000, [-0.2,3.2,-0.9,1.3])

print(solution['nodes']['n46'])