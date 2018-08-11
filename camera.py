from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 270
#camera.start_preview()
#sleep(10)
for i in range(1):
    sleep(1)
    camera.capture('/home/pi/Robo_Reef/Camera_Files/image%s.jpg' % i)
camera.stop_preview()
#camera.start_preview()
#camera.start_recording('/home/pi/Robo_Reef/Camera_Files/video.h264')
#sleep(10)
#camera.stop_recording()
#camera.stop_preview()
