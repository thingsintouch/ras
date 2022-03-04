import time
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.constants import PARAMS, PERIOD_DISPLAY_MANAGER
from common.params import Params

from display.helpers import Oled
from display.display_time import get_display_time

params = Params(db=PARAMS)
oled = Oled()

import RPi.GPIO as GPIO

class Relay():

    def __init__(self, pin):
        GPIO.setmode(GPIO.BOARD)  # GPIOs Nr by physical location
        GPIO.setup(pin, GPIO.OUT)  # set pin as output
        self.pin = pin
        params.put("relay_status", "0")
        self.send_output_to_GPIO(0)

    def display_status(self):
        time.sleep(PERIOD_DISPLAY_MANAGER)
        params.put("displayClock", "no")
        if self.status == 1:
            status_text = "ON"
        else:
            status_text = "OFF"
        message = f"\nRELAY\n{status_text}"
        oled.three_lines_text(message)
        time.sleep(get_display_time())
        params.put("displayClock", "yes")


    def send_output_to_GPIO(self,status):
        if status == 1:
            output = 0
        else:
            output = 1    
        GPIO.output(self.pin, output)
        self.status = status
        loggerINFO(f"Relay Hardware: status is {status} and GPIO {self.pin} output set to {output}")
        self.display_status()

    def relay_status_changed(self, current_status):
        if self.status != current_status:           
            return True
        else:
            return False
    
    def check_update_output(self):
        if params.get("relay_status") == "1":
            current_status = 1
        else:
            current_status = 0
        if self.relay_status_changed(current_status):
            self.send_output_to_GPIO(current_status)
