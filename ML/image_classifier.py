# -*- coding: utf-8 -*-
"""Image classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cwn3n3mhOFOhVFIsfPuHwct9cG-SL9VR
"""

#import all necessary modules and packages
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D,Dropout,Flatten,MaxPooling2D
#import tensorflow as tf
from tensorflow.keras.utils import to_categorical

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x

#load the mnist dataset in the variables from keras library

(x_train,y_train),(x_test,y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train.reshape(x_train.shape[0],28,28,1) #reshape both training and test set into 4-dim array of shape (60000,28,28,1)
x_test = x_test.reshape(x_test.shape[0],28,28,1)

x_train = x_train.astype('float32') #convert each value of the set into 32 bit floating point value
x_test = x_test.astype('float32')

x_train = x_train/255 #normalize each vector to bring the scale between [0,1] 
x_test = x_test/255

#Bulid a seqential model and attach different layers to the model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), input_shape=(28,28,1))) #used to extract features of the image
model.add(MaxPooling2D(pool_size=(2, 2))) #used to reduce the size of image
model.add(Conv2D(64, kernel_size=(3,3), input_shape=(28,28,1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten()) # Flattening the 2D arrays for dense or fully connected layers
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2)) #used to disable some neurons
model.add(Dense(10,activation='softmax'))

#used to compile the model
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])
model.optimizer.lr = 0.0002 #setting learning rate to 0.0002
#initializing the train values in the model

# Include the epoch in the file name (uses `str.format`)
checkpoint_path = "weights/cp-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights every 5 epochs
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, 
    verbose=1, 
    save_weights_only=True,
    period=3)

model.fit(x_train,
          y_train,
          epochs = 15,
          shuffle='True',
          callbacks=[cp_callback],
          validation_data=((x_test,y_test))
         )

model.save_weights(checkpoint_path.format(epoch=0))

#evaluate the model on test set
model.evaluate(x_test,y_test)