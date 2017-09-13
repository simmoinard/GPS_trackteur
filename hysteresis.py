import serial
import os
import time
import numpy as np
import csv
import time

## dd/mm/yyyy format
time = time.strftime("%d%m%y")


array = []
parcelle = []
with open("gps_experimentation/"+ str(time) + "-simple-log.txt") as f:
    for line in f:
        line = line.rstrip()
        spline = line.split(",")
        array.append(spline)

for i in range(0,len(array)):
    parcelle.append(array[i][2])
    array[i][1] = ((int(str(array[i][1])[:2])+2)*3600) + (int(str(array[i][1])[2:4])*60) + (int(str(array[i][1])[4:6]))

for i in range(0,len(array)):
    myset=list(set(parcelle[(i-4):(i+5)]))

    val = 0 #Hysteresis 1 : change the name of the parcel to the maximum of the 8 values around
    for j in range(len(myset)) :
        if parcelle[(i-4):(i+5)].count(myset[j]) > val :
            val = parcelle[(i-4):(i+5)].count(myset[j])
            array[i][2]=myset[j]

del array[:3]
actualparcel = parcelle[0]
j=0
for i in range(1,len(array)-1) :
    if array[i][2]!=array[i-1][2] : #regroup the data by the parcels
        with open("/home/pi/gps_experimentation/" + str(time) + "-grouped.txt", "a") as myfile :
            myfile.write(str(array[j][0]) + "," + str(int(array[i-1][1])-int(array[j][1])) + "," + array[j][2] + "\n")
        j=i
        actualparcel = array[i][2]
    lines = open("gps_experimentation/"+ str(time) + "-simple-log.txt").readlines() #remove the data seen
    open("gps_experimentation/"+ str(time) + "-simple-log.txt", 'w').writelines(lines[i:len(array)-1])


with open("/home/pi/gps_experimentation/" + str(time) + "-grouped.txt", "a") as myfile :
    myfile.write(str(array[j][0]) + "," + str(int(array[len(array)-1][1])-int(array[j][1])) + "," + array[j][2]+ "\n")
