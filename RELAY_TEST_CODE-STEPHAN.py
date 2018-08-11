#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)

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
o1=26
o2=19
o3=13
o4=6
o5=12
o6=16
o7=20
o8=21
gpioList = [o1, o3, o4, o5, o6, o7]#26 is outlet on top left, 19 is below 26, 13 is to the right of 26, 06 is below 13, etc.
print(gpioList)
for i in gpioList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)
for i in gpioList:
    print(GPIO.input(i))
    
Light_Red=o5
Light_White=o6
Fan_1=o7
Skimmer_B=o4
Skimmer_P=o3
#Skimmer ON for 6 hours then off

GPIO.output(Skimmer_B,1)
GPIO.output(Skimmer_P,1)
time.sleep(43200)
GPIO.output(Skimmer_B,0)
GPIO.output(Skimmer_P,0)
#Skimmer_B_OFF=GPIO.output(Skimmer_B,GPIO.LOW)

# Sleep time variables

#sleepTimeShort = 1
#sleepTimeLong = 3

# MAIN LOOP =====
# ===============
#GPIO.output(26, GPIO.HIGH) #26 is outlet on top left
#time.sleep(sleepTimeShort)
#GPIO.output(26, GPIO.LOW)
#time.sleep(sleepTimeShort)
#GPIO.output(19, GPIO.LOW) #19 is outlet on bottom left
#time.sleep(sleepTimeShort)
#GPIO.output(19, GPIO.HIGH)


