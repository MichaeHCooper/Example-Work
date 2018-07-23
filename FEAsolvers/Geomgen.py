"""
Geom generator for the finite elementanlysis software.
Started on Dec 5th 2016.
Aurthor: Michael Cooper.
"""

def beam(nodeapp):
    geom = {'nodes': {},
            'tris':  {},
            'forces':{},
            'props': {'E':200e9, 'v':(0.3), 't':(0.1)}}
    cellcount = 0
    while cellcount <= 15:
        geom['nodes']['n'+str(cellcount*3  )] = [cellcount*0.2, 0.0]
        geom['nodes']['n'+str(cellcount*3+1)] = [cellcount*0.2, 0.2]
        geom['nodes']['n'+str(cellcount*3+2)] = [cellcount*0.2, 0.4]
#        geom['forces']['n'+str(cellcount*3  )] = ['0','0']
#        geom['forces']['n'+str(cellcount*3+1)] = ['0','0']
#        geom['forces']['n'+str(cellcount*3+2)] = ['0','0']
        cellcount = cellcount+1
    cellcount = 0
    while cellcount < 15:
        t0 = [('n'+str(cellcount*3  )),('n'+str(cellcount*3+3)),('n'+str(cellcount*3+1))]
        t1 = [('n'+str(cellcount*3+3)),('n'+str(cellcount*3+4)),('n'+str(cellcount*3+1))]
        t2 = [('n'+str(cellcount*3+1)),('n'+str(cellcount*3+4)),('n'+str(cellcount*3+2))]
        t3 = [('n'+str(cellcount*3+4)),('n'+str(cellcount*3+5)),('n'+str(cellcount*3+2))]
        geom['tris']['t'+str(cellcount*4  )] = t0
        geom['tris']['t'+str(cellcount*4+1)] = t1
        geom['tris']['t'+str(cellcount*4+2)] = t2
        geom['tris']['t'+str(cellcount*4+3)] = t3
        cellcount = cellcount+1
    geom['forces']['n0'] = ['un','un']
    geom['forces']['n1'] = ['un','un']
    geom['forces']['n2'] = ['un','un']
    geom['forces'][nodeapp] = [0,-15e3]
    return geom