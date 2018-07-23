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