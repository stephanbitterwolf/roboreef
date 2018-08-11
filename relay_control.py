import numpy as np
import pandas as pd
import datetime 
import time
import RPi.GPIO as GPIO

#we need to add a line in here incase the input is nan and not float 

temp_data=pd.DataFrame.from_csv('STJ_Temp.csv')
def Day_temp_control(Temp_input,gpio_addresses): #feed the float temp and list of gpio pins for temp
    ts=time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    Month= int(time_stamp[5:7])
    Day = int(time_stamp[8:10])
    Hour = int(time_stamp[11:13])
    Month_index = temp_data['MM (mo)'] == Month
    Day_index = temp_data['DD (dy)'] == Day
    Hour_index = temp_data['hh (hr)'] == Hour
    current_time_temp = temp_data[Month_index & Day_index & Hour_index]
    Temp_reference =(float(current_time_temp['Average of WTMP (deg C)']))
    #Temp_reference=24
    print('Target temp',Temp_reference,float(Temp_input))
    if Temp_input > Temp_reference:
        for i in gpio_addresses:
            GPIO.output(i, 0)
            print(GPIO.input(i))
            print "Heater OFF" 
    elif Temp_input< Temp_reference:
        for i in gpio_addresses:
            GPIO.output(i, 1)
            print(GPIO.input(i))
            print "Heater ON" 
