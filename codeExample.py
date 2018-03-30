import numpy as np
import matplotlib.pyplot as plt
import random
from decimal import Decimal
import matplotlib.ticker as mtick
from scipy.interpolate import spline
from scipy.interpolate import pchip
import time
import math
import psutil

buckets = [];
initialVector = [];
numberOfComparisons = 0;
swapped = True;
numEntries = 0;
bucketCount = 0;
numRange = 0;
tracker = [];
imgNum = 0;
numberOfSwitches = 0;

def bubbleSort(bucket):
        global numberOfSwitches
        global numberOfComparisons
        swapped = True;
        for j in range(0,len(bucket)):
            numberOfComparisons+=1;
            if swapped == False:
                break;
            swapped = False;
            for i in range(0,len(bucket)-1):
                numberOfComparisons+=1;
                if bucket[i]>bucket[i+1]:
                    aux = bucket[i+1]
                    bucket[i+1] = bucket[i]
                    bucket[i] = aux
                    swapped = True;
        sA = bucket
        return sA

def bucketSort(array, bucketSize):
  if len(array) == 0:
    return array
    global bucketCount
    global buckets

  # Determine minimum and maximum values
  minValue = array[0]
  maxValue = array[0]
  for i in range(1, len(array)):
    if array[i] < minValue:
      minValue = array[i]
    elif array[i] > maxValue:
      maxValue = array[i]

  # Initialize buckets
  bucketCount = math.floor((maxValue - minValue) / bucketSize) + 1
  buckets = []
  for i in range(0, bucketCount):
    buckets.append([])

  # Distribute input array values into buckets
  for i in range(0, len(array)):
    buckets[math.floor((array[i] - minValue) / bucketSize)].append(array[i])

  # Sort buckets and place back into input array
  array = []
  for i in range(0, len(buckets)):
    bubbleSort(buckets[i])
    for j in range(0, len(buckets[i])):
      array.append(buckets[i][j])

  return array

bucketSize = [5,10,20,50,75,100,500,1000];
numEntries = [1000,2500,5000,10000,100000];

for buckets in bucketSize:
    for entries in numEntries:
       i = 0;
       while i<entries-1:    
            i+=1;
            initialVector.append(random.random()*1000000)
       start_time = time.time()
       orderedList = bucketSort(initialVector, buckets);
       timeTaken = time.time()-start_time
       print('%.2E' % Decimal(time.time()-start_time))
       tracker.append([buckets,timeTaken,bucketCount,entries,numberOfComparisons,numberOfSwitches])
       initialVector = [];
       numberOfComparisons = 0;
       numberOfSwitches = 0;
                
#-----------------------------------------------------------------------------
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d millions'))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%d k'))
plt.title('Bucket Sort Average (Random Input)')
plt.xlabel('Number of Entries')
plt.ylabel('Number of Comparisons')

startRange = 0
actualBucket = 0
plotLimits = len(bucketSize)
while actualBucket < plotLimits:
    listForBucketSize = tracker[startRange:len(numEntries)+startRange]
    startRange += len(numEntries)    
    currentEntry = 0;
    x = [];
    y = [];
    while(currentEntry < len(numEntries)):
        x.append(listForBucketSize[currentEntry][3]/1e03)
        y.append(listForBucketSize[currentEntry][4]/1e06)
        currentEntry+=1
    x = np.array(x);
    y = np.array(y);
    x_smooth = np.linspace(x.min(), x.max(), 1000)
    y_smooth = spline(x, y, x_smooth)
    plt.plot(x_smooth, y_smooth,lineWidth=1,
             label='Buckets: '+ str(listForBucketSize[0][2])
                   + ' | Bucket Size: '+str(listForBucketSize[0][0]) 
                   + ' | Comparisons: '+ str(listForBucketSize[len(listForBucketSize)-1][4]/1e06)[0:5] + ' M'

                   )
    actualBucket+=1;
plt.legend()
plt.savefig("plotWCase"+str(imgNum)+".png",dpi=300)
imgNum+=1
plt.show()