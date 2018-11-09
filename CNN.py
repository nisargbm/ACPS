# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import keras as k
from keras.models import Sequential
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, Dropout




train_path = 'C:/Users/Ravi Shankar Singh/Desktop/SEM VII/FYP/Dataset_Signature_Final/Dataset/dataset1'
valid_path = 'C:/Users/Ravi Shankar Singh/Desktop/SEM VII/FYP/Dataset_Signature_Final/Dataset/dataset2'
test_path  = ''

train_batches = ImageDataGenerator().flow_from_directory(train_path,target_size=(224,224),classes=['real','forge'],batch_size = 10)
valid_batches = ImageDataGenerator().flow_from_directory(valid_path,target_size=(224,224),classes=['real','forge'],batch_size = 10)
#test_batches  = ImageDataGenerator().flow_from_directory(test_path,targe_size=(224,224),classes=['Real','fake'],batch_size = 10)
  

imgs,labels = next(train_batches)

vgg16_model = k.applications.vgg16.VGG16()
model = Sequential()
for layer in vgg16_model.layers:
    model.add(layer)

model.layers.pop()
model.add(Dense(2,activation='softmax'))
adam = Adam(lr = 0.001)
model.compile(loss=k.losses.categorical_crossentropy,optimizer = adam,metrics=['accuracy'])
model.fit_generator(train_batches,steps_per_epoch = 6 ,validation_data= valid_batches,validation_steps = 6,epochs = 5 , verbose = 2)

