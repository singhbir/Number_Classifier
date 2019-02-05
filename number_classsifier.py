# -*- coding: utf-8 -*-
"""Number Classsifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AcAYwBiMbEUyIST3a53xm0BrEgMnhqDE
"""

import numpy as np
import matplotlib.pyplot  as plt
from sklearn import datasets
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from keras.datasets import mnist
from keras.layers import Flatten
from keras.layers import Dropout
from keras.models import Model
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
import random
# %matplotlib inline

data=mnist.load_data()

dir(data)

len(data[0][1])

(x_train,y_train),(x_test,y_test)=data

print(x_train.shape)
print(x_test.shape)

y_train.shape[0]

assert(x_train.shape[0]==y_train.shape[0]),"The number of images is not equal"
assert(x_train.shape[1:]==(28,28)),"The dimensions of the images are not 28*28"
assert(x_test.shape[0]==y_test.shape[0]),"The number of images is not equal"
assert(x_test.shape[1:]==(28,28)),"The dimensions of the images are not 28*28"



num_of_samples=[]
cols=5
num_classes=10

fig,axs=plt.subplots(nrows=num_classes,ncols=cols,figsize=(5,10))
fig.tight_layout()
for i in range(cols):
  for j in range(num_classes):
    x_selected=x_train[y_train==j]
    #print(len(x_selected))
    axs[j][i].imshow(x_selected[i,:,:])
    axs[j][i].axis("off")
    if i==2:
      axs[j][i].set_title(str(j))
      num_of_samples.append(len(x_selected))

x_train.shape

sd=x_train[y_train==0]

sd[0].shape

print(num_of_samples)
plt.figure(figsize=(12,4))
plt.bar(range(0,num_classes),num_of_samples)
plt.title("Distribution of the train dataset")
plt.xlabel("Class number")
plt.ylabel("Number of Images")

x_train=x_train.reshape(60000,28,28,1)
x_test=x_test.reshape(10000,28,28,1)   # image is converted into 3d

y_train=to_categorical(y_train,10)
y_test=to_categorical(y_test,10) # changing into categorical encoding 0--> 1 0 0 0 0 0 0 0 0   1 -->0 1 0 0 0 0 0 0 0 0

x_train=x_train/255 # to performe with more computation power
x_test=x_test/255

def le_net():
  model=Sequential()
  model.add(Conv2D(30,(5,5),input_shape = (28,28,1),activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Conv2D(15,(3,3),activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Flatten())
  model.add(Dense(500,activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dropout(0.3))#if you plot graph and you see that your accuracy or loss is not upto that mark then change dropout
  model.add(Dense(num_classes,activation='softmax')) #num_classes =10 it means jo result aayega vo 0-9 ke beech mein aayega . agar result mein yes or no aata to hum num_classes ko 2 kar dete
  model.compile(Adam(lr=0.01),loss='categorical_crossentropy',metrics=['accuracy']) # lr = learning rate
  return model

lenet =le_net()

lenet.summary()

history=lenet.fit(x_train,y_train,epochs=10,validation_split=0.1,batch_size=400,verbose=1,shuffle=1)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['loss','val_loss'])
plt.title('Loss')
plt.xlabel('epoch')
#blue line should not go beyond green line and blue line should be above green line if this is not the case then overfitting problem is there

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.legend(['acc','val_acc'])
plt.title('accuracy')
plt.xlabel('epoch')
#green line should be above blue line

import requests
from PIL import Image
from io import BytesIO

url="https://ak3.picdn.net/shutterstock/videos/23708593/thumb/1.jpg"
response = requests.get(url,stream=True)
img = Image.open(response.raw)
plt.imshow(img)

import cv2
img_array=np.asarray(img)
res=cv2.resize(img_array,(28,28))
gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
image=cv2.bitwise_not(gray)
plt.imshow(image,cmap=plt.get_cmap('gray'))

#img_array=cv2.resize(img_array,(28,28))

image=image/255
image=image.reshape(1,28,28,1)

lenet.predict_classes(image)





