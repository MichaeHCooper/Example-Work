"""
Structural solver for the building designer program.
Author - Michael Cooper
Created - 19th July 2017
"""

#################################### Setup ####################################

import numpy as np
import math as m

###############################################################################


################################### Solver ####################################

def BeamKLCS(MatProps,SecProps,DimProps,EndProps):
    """
    Assembles the beam stifness matrix in local coordinates. MatProps = (E, G, 
    nu), SecProps = (A, Iy, Iz, J, 'SecType'), DimProps = (B, D, L).
    """
    E  = MatProps[0]
    G  = MatProps[1]
    A  = SecProps[0]
    Iy = SecProps[1]
    Iz = SecProps[2]
    J  = SecProps[3]
    L  = DimProps[2]

    kx = E*A
    ky = E*Iy
    kz = E*Iz
    kt = G*J

    kx1 = kx/L
    kt1 = kt/L
    ky1 = 2*(ky/L)
    ky2 = 2*ky1
    ky3 = 3*(ky1/L)
    ky4 = 2*(ky3/L)
    kz1 = 2*(kz/L)
    kz2 = 2*kz1
    kz3 = 3*(kz1/L)
    kz4 = 2*(kz3/L)

    k = np.matrix(
       [[ kx1,   0,   0,   0,   0,   0,-kx1,   0,   0,   0,   0,   0],  # u1
        [   0, kz4,   0,   0,   0, kz3,   0,-kz4,   0,   0,   0, kz3],  # v1
        [   0,   0, ky4,   0,-ky3,   0,   0,   0,-ky4,   0,-ky3,   0],  # w1
        [   0,   0,   0, kt1,   0,   0,   0,   0,   0,-kt1,   0,   0],  # t x1
        [   0,   0,-ky3,   0, ky2,   0,   0,   0, ky3,   0, ky1,   0],  # t y1
        [   0, kz3,   0,   0,   0, kz2,   0,-ky3,   0,   0,   0, kz1],  # t z2
        [-kx1,   0,   0,   0,   0,   0, kx1,   0,   0,   0,   0,   0],  # u2
        [   0,-kz4,   0,   0,   0,-kz3,   0, kz4,   0,   0,   0,-kz3],  # v2
        [   0,   0,-ky4,   0, ky3,   0,   0,   0, ky4,   0, ky3,   0],  # w2
        [   0,   0,   0,-kt1,   0,   0,   0,   0,   0, kt1,   0,   0],  # t x2
        [   0,   0,-ky3,   0, ky1,   0,   0,   0, ky3,   0, ky2,   0],  # t y2
        [   0, kz3,   0,   0,   0, kz1,   0,-kz3,   0,   0,   0, kz2]]) # t z2
    BeamRelMask = []
    for i in range(3):
        if EndProps[i] == 0:
            BeamRelMask.append(i+3)
        if EndProps[i+3] == 0:
            BeamRelMask.append(i+9)
    k[BeamRelMask,:] = 0
    k[:,BeamRelMask] = 0
    return k

def BeamKGCS(kLCS, RotProps):
    """
    Assembles the stifnessmatrix in global coordinates given the stiffness
    matrix in the local coordinate system and the orientation of the element
    in 3D space. NOTE ALL ROTATIONS ARE COUNTER CLOCKWISE FROM BEAM FACING
    PARALLEL TO THE X AXIS IN A RIGHT HAND COORDINATE SYSTEM.
    """
    phi = RotProps[0] # Roll, CC
    tht = RotProps[1] # Pitch, CC
    psi = RotProps[2] # Yaw, CC

    cphi = m.cos(phi)
    sphi = m.sin(phi)
    ctht = m.cos(tht)
    stht = m.sin(tht)
    cpsi = m.cos(psi)
    spsi = m.sin(psi)

    r = np.matrix(
       [[ cpsi*ctht , cpsi*stht*sphi-spsi*cphi , cpsi*stht*cphi+spsi*sphi ],
        [ spsi*ctht , spsi*stht*sphi+cpsi*cphi , spsi*stht*cphi-cpsi*sphi ],
        [ -stht     , ctht*sphi                , ctht*cphi                ]])

    R = np.zeros((12,12))

    R[0:3,0:3] = r
    R[3:6,3:6] = r
    R[6:9,6:9] = r
    R[9:12,9:12] = r
    
    return R*kLCS*np.transpose(R)

def Assembly(Membs, Nodes):
    """
    Assembles the global stiffness matrix from the dictionaries of the members
    and nodes.  ASSUMES APON ASSEMBLY THAT THE SMALLEST NODE IS FIRST.
    """
    MembsLen = len(Membs)
    NodesLen = len(Nodes)
    KGlob = np.zeros((NodesLen*6,NodesLen*6))
    for i in range(MembsLen):
        K = BeamKLCS(Membs['M'+str(i)]['MatProps'],
                     Membs['M'+str(i)]['SecProps'],
                     Membs['M'+str(i)]['DimProps'],
                     Membs['M'+str(i)]['EndProps'])
        K = BeamKGCS(K, Membs['M'+str(i)]['RotProps'])
        Kaa = K[0:6,0:6]
        Kbb = K[6:12,6:12]
        Kab = K[0:6,6:12]
        Kba = K[6:12,0:6]
        a = int(Membs['M'+str(i)]['Nodes'][0][1])
        b = int(Membs['M'+str(i)]['Nodes'][1][1])
        KGlob[a*6:(a+1)*6, a*6:(a+1)*6] = KGlob[a*6:(a+1)*6, a*6:(a+1)*6]+Kaa
        KGlob[b*6:(b+1)*6, b*6:(b+1)*6] = KGlob[b*6:(b+1)*6, b*6:(b+1)*6]+Kbb
        KGlob[a*6:(a+1)*6, b*6:(b+1)*6] = KGlob[a*6:(a+1)*6, b*6:(b+1)*6]+Kab
        KGlob[b*6:(b+1)*6, a*6:(a+1)*6] = KGlob[b*6:(b+1)*6, a*6:(a+1)*6]+Kba
    return KGlob

def Solve(KGlob, Nodes):
    """
    Calculates the unknown nodal displacements.
    """
    NodesLen = len(Nodes)
    LGlob = np.zeros((NodesLen*6,1))
    UGlob = np.zeros((NodesLen*6,1))
    UMask = np.zeros(NodesLen*6)
    for i in range(NodesLen):
        L = np.reshape(np.array(Nodes['N'+str(i)]['Loading']),(6,1))
        U = np.array(Nodes['N'+str(i)]['Bounds'])
        LGlob[i*6:(i+1)*6,:] = L
        UMask[i*6:(i+1)*6] = U
    UMask = UMask.astype('int')
    UMask2 = []
    for i in range(len(UMask)):
        if UMask[i] == 0:
            UMask2.append(i)
    Kred = KGlob[UMask2]
    Kred = np.matrix(Kred[:,UMask2])
    Fred = np.matrix(LGlob[UMask2,:])
    try:
        Ured = Kred.I*Fred
    except:
        print(' WARNING MATRIX SINGULAR, STRUCTURE MAY BE STATICALLY'+
              ' INDETERMINATE.  EQUATION SOLVED USING SUDO INVERSE.\n')
        Ured = np.linalg.pinv(Kred)*Fred
    UGlob[UMask2,:] = Ured
    FGlob = np.array(np.matrix(KGlob)*UGlob)
    for i in range(NodesLen):
        FNode = tuple(np.reshape(FGlob[i*6:(i+1)*6],(6)))
        UNode = tuple(np.reshape(UGlob[i*6:(i+1)*6],(6)))
        Nodes['N'+str(i)]['Forces'] = FNode
        Nodes['N'+str(i)]['Disps'] = UNode

###############################################################################


################################ Misc Functions ###############################

def RecSecProps(DimProps):
    """
    Returns a tuple of the section properties for a given beam from a tuple of
    the dimensions. DimProps = (B, D, L)
    """
    B = DimProps[1]
    D = DimProps[0]
    a = B*D
    Iy = (D*B**3)/12.0
    Iz = (B*D**3)/12.0
    if B > D:
        J = (B*D**3)*(0.3333-0.21*(D/B)*(1.0-((D**4)/(12.0*B**4))))
    else:
        J = (D*B**3)*(0.3333-0.21*(B/D)*(1.0-((B**4)/(12.0*D**4))))
    return (a,Iy,Iz,J,'Rec')

def FillMatProps(E = None, G = None, nu = None):
    """
    Returns a tuple of the material properties, given two of the input
    properties.
    """
    if E == None:
        E = 2.0*G(1.0+nu)
    if nu == None:
        nu = (E/(2.0*G)) - 1.0
    if G == None:
        G = E/(2*(1.0+nu))
    return (E, G, nu)

###############################################################################


############################## Required Formats ###############################

"""
###############################################################################
The Solver requires that 'Membs' and 'Nodes' are in the following very precise
formats, to be used in the equation.

M0 = {'DimProps':(Breadth, Depth, Length),   - Beam Dimensions
      'RotProps':(Roll, Pitch, Yaw),         - Beam Orientation
      'EndProps':(Mx1,My1,Mz1,Mx2,My2,Mz2),  - Beam End Releases
      'SecProps':(a,Iy,Iz,J,Type)            - Section Properties
      'MatProps':(E, G, nu)                  - Material Propeties
      'Nodes'   :('N0','N1')               } - Nodes, LARGEST LAST

Membs = {'M0':M0, 'M1':M1...   ...'Mn':Mn}

N0 = {'Bounds'  :(u,v,w,thtx,thty,thtz),     - Boundaries, 1-Fixed, 0-Loose
      'Location':(x,y,z),                    - XYZ position of node
      'Loading' :(Fx,Fy,Fz,Mx,My,Mz),        - Applied Loads
      'Forces'  :(Fx,Fy,Fz,Mx,My,Mz),        - initially - 'unknown'
      'Disps'   :(u,v,w,thtx,thty,thtz),   } - initially - 'unknown'

Nodes = {'N0':N0, 'N1':N1...   ...'Nn':Nn}
###############################################################################
Solving Steps.

KGlobal = Assembly(Membs, Nodes) - Assembles the global stifness matrix

Solve(KGlobal, Nodes)            - Solves the equation and appends the nodal
                                 - forces and displacements to the Nodes dict.
###############################################################################
"""

###############################################################################