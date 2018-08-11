import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings
import numpy as np
import pandas as pd
import datetime

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
    f=open('masterdata.csv', 'w')
    f.write('Time, Temp_C, pH, ORP_mV,DO_mg,DO_PerSat,EC_uS,EC_PSU, \n')
    f.close()
    while True:
	    input = raw_input("Enter command: ")
	    if input.upper().startswith("LIST_ADDR"):
		    devices = device.list_i2c_devices()
		    for i in range(len (devices)):
			    print (devices[i])
			    
            elif input.upper().startswith("ALL"):
			delaytime = float(string.split(input, ',')[1])
		

			# check for polling time being too short, change it to the minimum timeout if too short
			if delaytime < AtlasI2C.long_timeout:
				print("Polling time is shorter than timeout, setting polling time to %0.2f" % AtlasI2C.long_timeout)
				delaytime = AtlasI2C.long_timeout

			# get the information of the board you're polling
			info = string.split(device.query("I"), ",")[1]
			print("Polling a sensor every %0.2f seconds, press ctrl-c to stop polling" % (delaytime))

                        
			try:
				while True:
                                        ts=time.time()
                                        time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                                        device.set_i2c_address(102)
                                        TRD=(device.query("R"))
                                        device.set_i2c_address(99)
                                        device.query("T,"+str(TRD))
                                        pH=(device.query("R"))
                                        print(device.query("T,?"))
                                        device.set_i2c_address(98)
                                        ORP=(device.query("R"))
                                        device.set_i2c_address(97)
                                        device.query("T,"+str(TRD))
                                        DO=(device.query("R"))
                                        print(device.query("T,?"))
                                        device.set_i2c_address(100)
                                        device.query("T,"+str(TRD))
                                        EC=(device.query("R"))
                                        print(device.query("T,?"))
                                        all_sensors= [time_stamp, TRD, pH, ORP, DO, EC ,'\n']
                                        all_sensor_string = ','.join(all_sensors)
                                        f=open('masterdata.csv', 'a')
                                        f.write(all_sensor_string)
                                        f.close()
					print(all_sensors)
					
					
			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous polling stopped")
                                

                            
				#temp_data=pd.DataFrame(temp_data)
				#temp_data.to_csv('TempPoll.csv')


if __name__ == '__main__':
	main()