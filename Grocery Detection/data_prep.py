
import os
import random
import sys
import cv2
import datetime 
import imutils

#allFiles = os.listdir("./data/version1/JPEGImages/")
#allFiles = r'C:/Users/baksh/Desktop/jetson-train-main/data/version1/JPEGImages/'

allFiles = os.listdir("./data/version3/JPEGImages")
print("allfiles:", allFiles)

imgCnt = len(allFiles)
testNum = int(imgCnt * 0.10)
testFileLst = []
while True:
    ap = random.choice(allFiles)
    #print(ap)
    if ap not in testFileLst:
        testFileLst.append(ap)
        print(testFileLst)
        if len(testFileLst) == testNum:
            break

trainFileLst = list(set(testFileLst).symmetric_difference(set(allFiles)))

f = open("./data/version3/ImageSets/Main/test.txt", 'w+')
for test in testFileLst:
    test = test.split(".")
    f.write(test[0] + "\n")
f.close()
f = open("./data/version3/ImageSets/Main/val.txt", 'w+')
for test in testFileLst:
    test = test.split(".")
    f.write(test[0] + "\n")
f.close()

f = open("./data/version3/ImageSets/Main/train.txt", 'w+')
for train in trainFileLst:
    train = train.split(".")
    f.write(train[0] + "\n")
f.close()
f = open("./data/version3/ImageSets/Main/trainval.txt", 'w+')
for train in trainFileLst:
    train = train.split(".")
    f.write(train[0] + "\n")
f.close()