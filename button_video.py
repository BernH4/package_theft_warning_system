import time
import subprocess
import RPi.GPIO as GPIO
from picamera import PiCamera

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the button pin (Adjust as necessary)
BUTTON_PIN = 19  # Change to your specific GPIO pin number

# Set up the button pin as an input with an internal pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

print("Press the button...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button is pressed (active low)
            print("Button Pressed! Recording video for 5 seconds...")
            
            # Start recording video
            camera.start_recording('video.h264')
            time.sleep(5)  # Record for 5 seconds
            camera.stop_recording()
            print("Recording stopped. Video saved as 'video.h264'")
            # Convert the .h264 video to .mp4 format using ffmpeg
            subprocess.run([ 'ffmpeg', '-y', '-i', 'video.h264', '-c:v', 'copy', 'video.mp4'
            ])
            print("Conversion complete. Video saved as 'video.mp4'")

            time.sleep(0.2)  # Debounce delay
        else:
            pass
finally:
    GPIO.cleanup()  # Clean up GPIO settings when done
