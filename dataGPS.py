import serial
import os
import matplotlib.path as mplPath
import numpy as np
import json
from pprint import pprint
import time

firstFixFlag = False # this will go true after the first GPS fix.
firstFixDate = ""

#set working directory
os.chdir('/home/pi')
#open geojson parcels, store in data
with open('parcelles.geojson') as data_file:
    data = json.load(data_file)

# Set up serial:
ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=4800,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)

# Helper function to take HHMM.SS, Hemisphere and make it decimal:
def degrees_to_decimal(data, hemisphere):
    try:
        decimalPointPosition = data.index('.')
        degrees = float(data[:decimalPointPosition-2])
        minutes = float(data[decimalPointPosition-2:])/60
        output = degrees + minutes
        if hemisphere is 'N' or hemisphere is 'E':
            return output
        if hemisphere is 'S' or hemisphere is 'W':
            return -output
    except:
        return ""

# Helper function to take a $GPRMC sentence, and turn it into a Python dictionary.
# This also calls degrees_to_decimal and stores the decimal values as well.
def parse_GPRMC(data):
    data = data.split(',')
    dict = {
            'fix_time': data[1],
            'validity': data[2],
            'latitude': data[3],
            'latitude_hemisphere' : data[4],
            'longitude' : data[5],
            'longitude_hemisphere' : data[6],
            'speed': data[7],
            'true_course': data[8],
            'fix_date': data[9],
            'variation': data[10],
            'variation_e_w' : data[11],
            'checksum' : data[12]
    }
    dict['decimal_latitude'] = degrees_to_decimal(dict['latitude'], dict['latitude_hemisphere'])
    dict['decimal_longitude'] = degrees_to_decimal(dict['longitude'], dict['longitude_hemisphere'])
    return dict

# Main program loop:
while True:

    line = ser.readline()
    if "$GPRMC" in line: # This will exclude other NMEA sentences the GPS unit provides.
        gpsData = parse_GPRMC(line) # Turn a GPRMC sentence into a Python dictionary called gpsData
        if gpsData['validity'] == "A": # If the sentence shows that there's a fix, then we can log the line
            if firstFixFlag is False: # If we haven't found a fix before, then set the filename prefix with GPS date & time.
                firstFixDate = gpsData['fix_date'] # + "-" + gpsData['fix_time']
                firstFixFlag = True
            else: # write the data to a simple log file and then the raw data as well:
		gpsData['fix_time'] = int(float(gpsData['fix_time'])) #+ 20000
        time.sleep(1) #sleep for 1 second
        #Loop for every parcel
        for i in range(0,len(data["features"])-1) :
            CRD = data["features"][i]["geometry"]["coordinates"][0][0] #store coordinates in CRD
            coordx = gpsData['decimal_longitude'] #store longitude in coordx
            coordy = gpsData['decimal_latitude']  #store latitude in coordx
            #print(gpsData['decimal_latitude'],gpsData['decimal_longitude'])
            bbPath = mplPath.Path(np.array(CRD)) #arrange coordinates for path
            val = bbPath.contains_point((coordx,coordy)) #verify if point is in the polygon i
            if (val is True) :
                with open("/home/pi/gps_experimentation/" + firstFixDate + "-simple-log.txt", "a") as myfile:
                    myfile.write(gpsData['fix_date'] + "," + str(gpsData['fix_time']) + "," + data["features"][i]["properties"]["CODE"] + "," +"\n")
                print (data["features"][i]["properties"]["CODE"]) #print the parcel if the point is in the polygon
    #pour chaque parcelle
