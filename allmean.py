import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings
import numpy as np
import pandas as pd
import datetime
from warningsystem import email_alert, warning_log, email_template
from database import database_write
import RPi.GPIO as GPIO
from relay_control import Day_temp_control

class AtlasI2C:
	long_timeout = 1.5         	# the timeout needed to query readings and calibrations
	short_timeout = .5         	# timeout for regular commands
	default_bus = 1         	# the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
	default_address = 98     	# the default address for the sensor (sensor 98 is the pH sensor)
	current_addr = default_address
	

	def __init__(self, address=default_address, bus=default_bus):
		# open two file streams, one for reading and one for writing
		# the specific I2C channel is selected with bus
		# it is usually 1, except for older revisions where its 0
		# wb and rb indicate binary read and write
		self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
		self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

		# initializes I2C to either a user specified or default address
		self.set_i2c_address(address)

	def set_i2c_address(self, addr):
		# set the I2C communications to the slave specified by the address
		# The commands for I2C dev using the ioctl functions are specified in
		# the i2c-dev.h file from i2c-tools
		I2C_SLAVE = 0x703
		fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
		fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
		self.current_addr = addr

	def write(self, cmd):
		# appends the null character and sends the string over I2C
		cmd += "\00"
		self.file_write.write(cmd)

	def read(self, num_of_bytes=31):
		# reads a specified number of bytes from I2C, then parses and displays the result
		res = self.file_read.read(num_of_bytes)         # read from the board
		response = filter(lambda x: x != '\x00', res)     # remove the null characters to get the response
		if ord(response[0]) == 1:             # if the response isn't an error
			# change MSB to 0 for all received characters except the first and get a list of characters
			char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
			# NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
			return " "+ ''.join(char_list)     # convert the char list to a string and returns it
		else:
			return "Error " + str(ord(response[0]))

	def query(self, string):
		# write a command to the board, wait the correct timeout, and read the response
		self.write(string)

		# the read and calibration commands require a longer timeout
		if((string.upper().startswith("R")) or
			(string.upper().startswith("CAL"))):
			time.sleep(self.long_timeout)
		elif string.upper().startswith("SLEEP"):
			return "sleep mode"
		else:
			time.sleep(self.short_timeout)

		return self.read()

	def close(self):
		self.file_read.close()
		self.file_write.close()

	def list_i2c_devices(self):
		prev_addr = self.current_addr # save the current address so we can restore it after
		i2c_devices = []
		for i in range (0,128):
			try:
				self.set_i2c_address(i)
				self.read()
				i2c_devices.append(i)
			except IOError:
				pass
		self.set_i2c_address(prev_addr) # restore the address we were using
		return i2c_devices
	

        
def main():
    device = AtlasI2C()
    #f=open('30_sample_mean.csv', 'w')
    #f.write('Time, TRD (C), pH, ORP (mV), DO (mg/L),DO (%Sat),EC (uS), EC (PSU), \n')
    #f.close()
    def check_data(result):
        if "Error" in result:
                return np.nan
        else:
                return float(result)

    while True:
	    input = "All,6,0,0,0,0,0,0,0,0"#raw_input("Enter command, sample rate (sample/x seconds), and each relay use (temp, 0) 1-8 (no spaces): ")
	    if input.upper().startswith("LIST_ADDR"):
		    devices = device.list_i2c_devices()
		    for i in range(len (devices)):
			    print (devices[i])
			    
            elif input.upper().startswith("ALL"):
			delaytime = float(string.split(input, ',')[1])
                        GPIO.setmode(GPIO.BCM) #referring to the pins by the "Broadcom SOC channel" 
                        temp_relay =[] #make empty inputs for relays
                        off_relay =[]
                        for i in range(len(string.split(input,','))):
                                if (string.split(input,',')[i]) == "0":
                                        off_relay.append(i-1)
                                elif (string.split(input,',')[i]) == "temp":
                                        temp_relay.append(i-1)
                        gpio_pins =[26,19,13,06,12,16,20,21]
                        temp_gpio_pins = [gpio_pins[i-1] for i in temp_relay] #this sets a list of gpio addresses for temp relays
                        off_gpio_pins = [gpio_pins[i-1] for i in off_relay]
                        for i in temp_gpio_pins: #set up all gpios for heaters
                                GPIO.setup(i, GPIO.OUT)                    
# GPIO | Relay
#--------------
# 26     01
# 19     02
# 13     03
# 06     04
# 12     05
# 16     06
# 20     07
# 21     08

# initiate list with pin gpio pin numbers

			# check for polling time being too short, change it to the minimum timeout if too short
			if delaytime < AtlasI2C.long_timeout:
				print("Polling time is shorter than timeout, setting polling time to %0.2f" % AtlasI2C.long_timeout)
				delaytime = AtlasI2C.long_timeout

			# get the information of the board you're polling
			info = string.split(device.query("I"), ",")[1]
			print("Polling a sensor every %0.2f seconds, recording average of 30 reads. press ctrl-c to stop polling" % (delaytime))

                        
			try:
                                TRD=[]
                                pH=[]
                                DO=[]
                                DO2=[]
                                EC=[]
                                EC2=[]
                                ORP=[]
                                Time=[]
                                
				while True:                                        
                                        ts=time.time()
                                        time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                                        Time.append(time_stamp)
                                        
                                        device.set_i2c_address(102)
                                        TRD.append(check_data(device.query("R")))
                                        length=[len(TRD)]
                                        cal_temp= TRD[-1]
                                                                               
                                        device.set_i2c_address(99)
                                        device.query("T,"+str(cal_temp))
                                        pH.append(check_data(device.query("R")))
                                        
                                        device.set_i2c_address(98)
                                        ORP.append(check_data(device.query("R")))
                                        
                                        device.set_i2c_address(100)
                                        device.query("T,"+str(cal_temp))
                                        EC_raw=(device.query("R"))
                                        if "Error" in EC_raw:
                                                EC.append(np.nan)
                                                EC2.append(np.nan)
                                        else:
                                                EC.append(float(EC_raw.split(',')[0]))
                                                EC2.append(float(EC_raw.split(',')[1]))
                                        ec_comp=EC[-1]
                                        
                                        device.set_i2c_address(97)
                                        device.query("T,"+str(cal_temp))
                                        device.query("S,"+str(ec_comp))
                                        DO_raw=(device.query("R"))
                                        if "Error" in DO_raw:
                                                DO.append(np.nan)
                                                DO2.append(np.nan)
                                        else:
                                                DO.append(float(DO_raw.split(',')[0]))
                                                DO2.append(float(DO_raw.split(',')[1]))
                                        
                                        print([Time[-1],TRD[-1],pH[-1],ORP[-1],DO[-1],DO2[-1],EC[-1],EC2[-1]])
                                        
                                        #print(all_sensors[1:8, -1])
                                        if len(TRD) >1:
                                                last=len(TRD)-1
                                                TRDav = str(np.nanmean(TRD[last]))
                                                pHav = str(np.nanmean(pH[last]))
                                                ORPav = str(np.nanmean( ORP[last]))
                                                DOav = str(np.nanmean(DO[last]))
                                                DO2av = str(np.nanmean(DO2[last]))
                                                ECav = str(np.nanmean(EC[last]))
                                                EC2av = str(np.nanmean(EC2[last]))
                                                Day_temp_control(float(TRDav),temp_gpio_pins)
                                                last_call =[time_stamp,TRDav,pHav,ORPav, DOav,DO2av,ECav, EC2av,'\n']
                                                database_entry=(time_stamp[:10],time_stamp[11:],TRDav,pHav,ORPav, DOav,DO2av,ECav, EC2av)
                                                all_sensor_string = ','.join(last_call)
                                                database_write(database_entry)
                                                f=open('30_sample_mean.csv', 'a')
                                                f.write(all_sensor_string)
                                                f.close()
                                        if len(TRD) > 15:
                                                TRDav = str(np.nanmean(TRD))
                                                pHav = str(np.nanmean(pH))
                                                ORPav = str(np.nanmean( ORP))
                                                DOav = str(np.nanmean(DO))
                                                DO2av = str(np.nanmean(DO2))
                                                ECav = str(np.nanmean(EC))
                                                EC2av = str(np.nanmean(EC2))
                                                
                                                all_sensors_mean= [TRDav, pHav, ORPav, DOav, DO2av, ECav, EC2av]

                                                email_alert(all_sensors_mean)
                                        

                                                
                                                TRD=[]
                                                pH=[]
                                                DO=[]
                                                DO2=[]
                                                EC=[]
                                                EC2=[]
                                                ORP=[]        

				 	
					
					
					
			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous polling stopped")
                                

                            


if __name__ == '__main__':
	main()
