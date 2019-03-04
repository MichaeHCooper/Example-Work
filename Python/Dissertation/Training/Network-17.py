"""
"Bot The Builder"

Neural network based on the YOLO network architecture.

Created - 03.04.2018
Author  - Michael Cooper
"""

import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import keras.backend as K
import numpy as np
import Utils

###############################################################################

def createmodel():
    """
    Creates the BTB network architecture.

    In  - [Z,160,160, 1]
    Out - [Z, 5, 5,13]
    """

    model = Sequential()

    # 160x106 Layers

    model.add(Conv2D(filters = 25, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same',
                     input_shape=(160,160,1)))
    model.add(BatchNormalization())

    # 80x80 Layers

    model.add(MaxPooling2D(pool_size = (2, 2), strides = (2,2)))

    model.add(Conv2D(filters = 50, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    # 40x40 Layers
    
    model.add(MaxPooling2D(pool_size = (2, 2), strides = (2,2)))

    model.add(Conv2D(filters = 100, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 50, kernel_size = (1, 1), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 100, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    # 20x20 Layers

    model.add(MaxPooling2D(pool_size = (2, 2), strides = (2,2)))

    model.add(Conv2D(filters = 200, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 100, kernel_size = (1, 1), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 200, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    # 10x10 Layers

    model.add(MaxPooling2D(pool_size = (2, 2), strides = (2,2)))

    model.add(Conv2D(filters = 400, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 200, kernel_size = (1, 1), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 400, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 200, kernel_size = (1, 1), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 400, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    # 5x5 Layers

    model.add(MaxPooling2D(pool_size = (2, 2), strides = (2,2)))

    model.add(Conv2D(filters = 800, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 400, kernel_size = (1, 1), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 800, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 400, kernel_size = (1, 1), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    model.add(Conv2D(filters = 800, kernel_size = (3, 3), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    # Output Layers

    model.add(Conv2D(filters = 13, kernel_size = (1, 1), strides = (1,1),
                     activation = 'relu', padding = 'same'))
    model.add(BatchNormalization())

    # Compiler

    model.compile(loss=BTBloss,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
    return model

def train(Xfilename,Yfilename,model,run,epochs,batchsize):
    """
    trains the model given training data.
    """
    X = np.load(Xfilename)
    Y = np.load(Yfilename)
    print(np.shape(X))
    print(np.shape(Y))
    checkpointer = keras.callbacks.ModelCheckpoint(
               run+'BTB{epoch:02d}.hdf5',save_weights_only=True)
    model.fit(X, Y, batch_size = batchsize, epochs = epochs,
          callbacks=[checkpointer])

def loadmodel(filename, model):
    """
    loads saved weights into the model.
    """
    return model.load_weights(filename)

def evaluate(Xfilename,Yfilename,model):
    """
    Evaluates the model returning the loss of a testing data set.
    """
    X = np.load(Xfilename)
    Y = np.load(Yfilename)
    print(np.shape(X))
    print(np.shape(Y))
    return model.evaluate(X,Y)

###############################################################################

def BTBloss(y_true,y_pred):
    """
    Defines a custom loss function for the model.  The loss function is
    identical to the YOLO loss function with the addition of an extra term
    relating to the rotation of the bounding boxes.
    """

    # Dimensions are all linear error.
    objMask0 = y_true[:,:,:,5]
    MaskShape0 = K.shape(objMask0)
    Zeros0 = K.zeros(MaskShape0)
    notMask0 = K.equal(y_true[:,:,:,5],Zeros0)
    notMask0 = K.cast(notMask0, 'float32')

    objMask1 = y_true[:,:,:,11]
    MaskShape1 = K.shape(objMask1)
    Zeros1 = K.zeros(MaskShape1)
    notMask1 = K.equal(y_true[:,:,:,11],Zeros1)
    notMask1 = K.cast(notMask1, 'float32')

    lamcoord = 5
    lamdims = 5
    lamtheta = 10
    lamobj = 0.5
    lamnoobj = 0.5
    lamp = 1.0

    coords = ( objMask0*(K.abs(y_true[:,:,:,2]-y_pred[:,:,:,2])+K.abs(y_true[:,:,:,3]-y_pred[:,:,:,3]))+
               objMask1*(K.abs(y_true[:,:,:,8]-y_pred[:,:,:,8])+K.abs(y_true[:,:,:,9]-y_pred[:,:,:,9])) )
    coords = K.sum(coords,1)
    coords = lamcoord*K.sum(coords,1)

    dims = ( objMask0*(K.abs(y_true[:,:,:,0]-y_pred[:,:,:,0])+K.abs(y_true[:,:,:,1]-y_pred[:,:,:,1]))+
             objMask1*(K.abs(y_true[:,:,:,6]-y_pred[:,:,:,6])+K.abs(y_true[:,:,:,7]-y_pred[:,:,:,7])) )
    dims = K.sum(dims,1)
    dims = lamdims*K.sum(dims,1)

    theta = ( objMask0*K.abs(y_true[:,:,:,4]-y_pred[:,:,:,4])+
              objMask1*K.abs(y_true[:,:,:,10]-y_pred[:,:,:,10]) )
    theta = K.sum(theta,1)
    theta = lamtheta*K.sum(theta,1)

    # The predictors are all quadratic clasification error.
    conf = ( objMask0*(y_true[:,:,:,5]-y_pred[:,:,:,5])**2+
             objMask1*(y_true[:,:,:,11]-y_pred[:,:,:,11])**2 )
    conf = K.sum(conf,1)
    conf = lamobj*K.sum(conf,1)

    cnot = ( notMask0*(y_true[:,:,:,5]-y_pred[:,:,:,5])**2+
             notMask1*(y_true[:,:,:,11]-y_pred[:,:,:,11])**2 )
    cnot = K.sum(cnot,1)
    cnot = lamnoobj*K.sum(cnot,1)

    p = (y_true[:,:,:,12]-y_pred[:,:,:,12])**2
    p = K.sum(p,1)
    p = lamp*K.sum(p,1)

    return (coords + dims + theta + conf + cnot + p)

###############################################################################

def test(model,threshold,Z):
    """
    Provides a graphical based way of quickly checking the models performance.
    """
    Data = Utils.DataGrid(160,5)
    Xtrue,Ytrue = Data.createdata(Z,2)
    Ypred = model.predict(Xtrue)
    Ypred = Ypred[0]
    Ypredlist = []
    Ytrue = Ytrue[0]
    Ytruelist = []
    for i in Ypred:
        for j in i:
            k = list(j)
            out0 = k[:5]
            out0.append(k[5]*k[12])
            out1 = k[6:11]
            out1.append(k[11]*k[12])
            Ypredlist.append(out0)
            Ypredlist.append(out1)
    for i in Ytrue:
        for j in i:
            k = list(j)
            out0 = k[:5]
            out0.append(k[5]*k[12])
            out1 = k[6:11]
            out1.append(k[11]*k[12])
            Ytruelist.append(out0)
            Ytruelist.append(out1)
    for i in Ytruelist:
        if i[-1] > 0.5:
            print('w:'+str(round(i[0],3))+',  h:'+str(round(i[1],3))+
               ',  x:'+str(round(i[2],3))+',  y:'+str(round(i[3],3))+
               ',  t:'+str(round(i[4],3))+',  C:'+str(round(i[5],3))+
               '   Ground Truth')
            vecs = Data.boxverticies(i[0],i[1],i[2],i[3],i[4])
            Utils.DataPlot.plotbox(160,vecs,colour='b')
    for i in Ypredlist:
        if i[-1] > threshold:
            print('w:'+str(round(i[0],3))+',  h:'+str(round(i[1],3))+
               ',  x:'+str(round(i[2],3))+',  y:'+str(round(i[3],3))+
               ',  t:'+str(round(i[4],3))+',  C:'+str(round(i[5],3))+
               '   Predicted')
            vecs = Data.boxverticies(i[0],i[1],i[2],i[3],i[4])
            Utils.DataPlot.plotbox(160,vecs,colour='r')

###############################################################################

"""
Training and testing
"""


BTB = createmodel()

loadmodel('Version2NBTB10.hdf5',BTB)

train('X20K-5.npy','Y20K-5.npy',BTB,'Version2O',20,100)

results = evaluate('X1K-5','Y1K-5',BTB)

print(results)

test(BTB,0.5,[1])