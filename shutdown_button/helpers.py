import RPi.GPIO as GPIO
import time
from common.constants import (
    PIN_SHUTDOWN_BUTTON,
    PIN_POWER_FOR_SHUTDOWN_BUTTON
)

# Define GPIO pins
pin_shutdown_button = PIN_SHUTDOWN_BUTTON  
pin_power_for_shutdown_button = PIN_POWER_FOR_SHUTDOWN_BUTTON

def setup_GPIO_shutdown_button():
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_shutdown_button, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(pin_power_for_shutdown_button, GPIO.OUT)
    # Provide power to the switch
    GPIO.output(pin_power_for_shutdown_button, GPIO.HIGH)

def is_shutdown_button_pressed():
    input_state = GPIO.input(pin_shutdown_button)
    print(input_state)
    if input_state == GPIO.LOW:
        print("Button Pressed")
        time.sleep(0.1)  # Add a small delay to debounce the button
        return True
    return False

def cleanup_GPIO():
    # Cleanup GPIO
    GPIO.output(pin_power_for_shutdown_button, GPIO.LOW)  # Turn off power to the switch
    GPIO.cleanup()

def set_for_shutdown():
    print("#"*100)
    print("set for shutdown")
    print("#"*100)
