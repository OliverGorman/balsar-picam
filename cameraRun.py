from picamera import PiCamera
from gpiozero import LED, Button
from threading import Thread
from time import sleep
from datetime import datetime
import os

def wait_button() :
    button = Button(21)
    button.wait_for_press()
    camera.stop_recording()
    camera.close()
    os.system("sudo shutdown now")
    exit(1)


def blink_led() :
	led = LED(4)
	while True:
		led.on()
		sleep(1)
		led.off()
		sleep(1)

INTERVAL = 30
camera = PiCamera(framerate=20,resolution=(1280,720))
camera.start_preview()
print("Recording")
camera.start_recording("videos/"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"-1.h264", sei=True)
Thread(target=blink_led, daemon=True).start()
Thread(target=wait_button, daemon=True).start()
camera.stop_preview()

camera.wait_recording(INTERVAL)

counter = 1
try:
	while True:
		counter += 1
		camera.split_recording("videos/"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"-"+str(counter)+".h264")
		camera.wait_recording(INTERVAL)
		
# Handles the case when user exits the running script using Control+C
except KeyboardInterrupt:
	camera.stop_recording()

	camera.close()
