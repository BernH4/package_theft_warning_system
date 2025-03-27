import time
import RPi.GPIO as GPIO

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the button pin (Adjust as necessary)
BUTTON_PIN = 19  # Change to your specific GPIO pin number

# Set up the button pin as an input with an internal pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press the button...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button is pressed (active low)
            print("Button Pressed!")
            time.sleep(0.2)  # Debounce delay
        else:
            pass
finally:
    GPIO.cleanup()  # Clean up GPIO settings when done
