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
print("Recording")

Thread(target=blink_led, daemon=True).start()
Thread(target=wait_button, daemon=True).start()

counter = 1
try:
	while True:
		
		file_name = f"videos/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{str(counter)}"

		if counter == 1 :
			camera.start_recording(f"{file_name}.h264", sei=True)
		else :
			camera.split_recording(f"{file_name}.h264")

		camera.wait_recording(INTERVAL)

		os.rename(f"{file_name}.h264", f"{file_name}.mp4")
		counter += 1
		
# close gracefully
finally :
	camera.stop_recording()
	os.rename(f"{file_name}.h264", f"{file_name}.mp4")

	camera.close()
