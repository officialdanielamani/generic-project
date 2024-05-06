# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 01:29:34 2024

@author: PC
"""

import serial
# Open serial port
# 'COM11' replace with your port
ser = serial.Serial('COM11', 9600, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            
            line = ser.readline().decode('utf-8').rstrip()
            line = line.rstrip("\r\n")
            line_arry= line.split(";") # We spilt using ;
            # Example data come in COM
            # Hello;123;35.255;60.27;Test  
            # Create a dictionary with the data (example JSON with 5 data)
            line_arry= line.split(";")
            
            data_1 = "ID=" + line_arry[0] #Hello
            data_2 = "Location=" + line_arry[1] #123    
            data_3 = "Code=" + line_arry[2] #35.255
            data_4 = "Name=" + line_arry[3] #60.27
            data_5 = "Temperature=" + line_arry[4] #Test


            data_all =  data_1 + data_2 + data_3 + data_4 + data_5
            print(data_all)
             
except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    ser.close()
