import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
print(GPIO.OUT)
GPIO.output(26,1)

