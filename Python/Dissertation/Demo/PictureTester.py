"""
Stripped Piocture Tester for Demo

Author - Michael Cooper
Created - 14.04.2018
"""

import numpy as np
import Utilities
import matplotlib.pyplot as plt
import Network as Net
import matplotlib

def LoadModel(weights):
    model = Net.createmodel()
    model.load_weights(weights)
    return model

def testpic(img, model, threshold):
    img = np.reshape(img, (1,160,160,1))
    Data = Utilities.DataGrid(160,5)
    Ypred = model.predict(img)
    Ypred = Ypred[0]
    Ypredlist = []
    for i in Ypred:
        for j in i:
            k = list(j)
            out0 = k[:5]
            out0.append(k[5]*k[12])
            out1 = k[6:11]
            out1.append(k[11]*k[12])
            Ypredlist.append(out0)
            Ypredlist.append(out1)
    for i in Ypredlist:
        if i[-1] > threshold:
            vecs = Data.boxverticies(i[0],i[1],i[2],i[3],i[4])
            Utilities.DataPlot.plotbox(160,vecs,colour='r',scale=160.0)

def test(img, model, threshold):
    img = img
    testpic(img, model, threshold)
    plt.imshow(img, cmap="binary")
    plt.axis('off')
    plt.savefig('temp.png',bbox_inches='tight')
    plt.clf()
