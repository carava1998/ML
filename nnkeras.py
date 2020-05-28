# -*- coding: utf-8 -*-
"""NNKeras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A6cJywMhmvevI1DRZiz1EX30L0xkNguv
"""

from keras import models
from keras import layers
import keras
from csv import reader
from keras.utils import to_categorical
import numpy

"""The next block of code is the one that is in charge of cleaning, building, spliting and scaling the ds"""

def load_csv(filename):
  """ This function cleans the dataset from the rows that have Null and retur a clean dataset"""
  dataset = []
  with open(filename, 'r') as file:
    csvReader =  reader(file)
    for row in csvReader:
      if (not row) or ("NA" in row):
        continue
      dataset.append(row[3:])
  dataset.pop(0)#This is to skip the names of the columns
  return dataset


def str_column_to_float(dataset):#This changes all the values to float values, to avoid problems with max function
  for i in range(len(dataset[0])):
    for row in dataset:
      row[i] = float(row[i].strip())

def scale(dataset): #this gives us values between -1 and 1
  minmax = []
  for i in range(len(dataset[0])): #This is looking in each column, row example:['0', '39', '4', '1', '9', '0', '0', '0', '0', '170', '110.5', '69', '22.19', '60', '103', '0']
    columnValues = [row[i] for row in dataset]
    acum = 0
    for row in columnValues:
      acum += row
    value_min = min(columnValues)
    value_max = max(columnValues)
    minmax.append([value_min, value_max])
  for row in dataset:
    for i in range(len(row)):
      if(minmax[i][0] != 1 and (minmax[i][1] - minmax[i][0]) != 0 ):
         row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0]) 
  

def getYX(ds):
  y = []
  for row in ds:
    temp = row.pop(len(row)-1)
    y.append(temp)
  return y

def splitDs (dataset,splits):
  splitData = []
  cpyDs = list(dataset)
  splitSize = int(len(dataset)/splits)
  for i in range(splits):
    split= []
    for j in range(splitSize):
      split.append(cpyDs.pop())
    splitData.append(split)
  return splitData

def getDs(filename): #Build the complete and clean ds
  ds = load_csv(filename)
  str_column_to_float(ds)
  scale(ds)
  return splitDs(ds,2)

network = models.Sequential()
network.add(layers.Dense(128,activation='tanh', input_shape=(36,)))
network.add(layers.Dense(64,activation='tanh'))
network.add(layers.Dense(32,activation='tanh'))
network.add(layers.Dense(16,activation='tanh'))
network.add(layers.Dense(4,activation='softmax'))



ds = getDs("CTG.csv")

dsTrainY = getYX(ds[0])
dsTrainY = numpy.asarray(dsTrainY).astype('float32')
#dsTrainY = to_categorical(dsTrainY)
print("Train Label Shape", dsTrainY.shape)

dsTrainX = ds[0]
dsTrainX = numpy.array(dsTrainX)
print("Train In Shape",dsTrainX.shape)


dsTestY = getYX(ds[1])
dsTestY = numpy.asarray(dsTestY).astype('float32')
#dsTestY = to_categorical(dsTestY)
print("Test Labels Shape", dsTestY.shape)


dsTestX = ds[1]
dsTestX = numpy.array(dsTestX)
print("Test In Shape",dsTestX.shape)

network.summary()
opti = keras.optimizers.Adam(learning_rate=0.0001)
network.compile(optimizer=opti,
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy'])

network.fit(dsTrainX,dsTrainY,validation_data=(dsTestX,dsTestY),epochs = 25)

test_loss, test_acc = network.evaluate(dsTestX, dsTestY)
print ('test_acc:', test_acc, ' test_loss:', test_loss)

for i in range(1000):
  if(dsTestY[i] == 3.0):
    print(i)

arr = [dsTestX[118]]
arr = numpy.array(arr)
auxArr = network.predict(arr)
index0=numpy.argmax(auxArr[0])
print(index0)

# index1=numpy.argmax(auxArr[1])
#index2=numpy.argmax(auxArr[2])


# print(index0,index1,index2)

