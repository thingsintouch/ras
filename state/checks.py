import os
import time
import sys

from display.helpers import sh1106

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from common import constants as co

from common.params import Params
from odoo.odooRequests import check_if_registered
from common.connectivity import isPingable


params = Params(db=co.PARAMS)

list_of_boolean_flags = [
    "shouldGetFirmwareUpdate",
    "rebootTerminal",
    "partialFactoryReset",
    "fullFactoryReset",
    "shutdownTerminal",
]

def display_off():
    try:
        display = sh1106()
        display.display_off()
    except Exception as e:
        loggerINFO(f"could not execute -display_off- before shutdown or reboot: {e}")   

def set_all_boolean_flags_to_false():
    for flag in list_of_boolean_flags:
        params.put(flag, "0")

class Status_Flags_To_Check():

    def __init__(self):
        self.acknowledged = False
        self.tz = params.get("tz")
        self.action_for_boolean_flag = {
            "shouldGetFirmwareUpdate"   : self.shouldGetFirmwareUpdate,
            "shutdownTerminal"          : self.shutdownTerminal,
            "rebootTerminal"            : self.rebootTerminal,
            "partialFactoryReset"       : self.partialFactoryReset,
            "fullFactoryReset"          : self.fullFactoryReset,
        }

    def check(self):
        self.check_if_registered_once_after_every_launch()
        for boolean_flag in list_of_boolean_flags:
            if params.get(boolean_flag) == "1":
                set_all_boolean_flags_to_false()
                display_off()
                loggerINFO("-"*20 + boolean_flag + "#"*20)
                self.action_for_boolean_flag[boolean_flag]()
                time.sleep(20)
                sys.exit(0)

    def check_if_registered_once_after_every_launch(self):
        if not self.acknowledged:
            if check_if_registered():
                params.put("acknowledged", "1")
                self.acknowledged = True

    def shouldGetFirmwareUpdate(self):
        if isPingable("github.com"):
            loggerINFO("<<<<++++++++ Firmware Update +++++++>>>>>>")
            os.chdir(co.WORKING_DIR)
            os.system("sudo git pull")
            display_off()
            time.sleep(1)
            self.rebootTerminal()
        else:
            loggerINFO("Firmware Update not possible: GitHub is down")   

    def shutdownTerminal(self):
        loggerINFO("-----############### shutdownTerminal ###############------")
        os.system("sudo shutdown now")
        time.sleep(60)
        sys.exit(0)

    def rebootTerminal(self):
        loggerINFO("-----############### rebootTerminal ###############------")
        os.system("sudo reboot")
        time.sleep(60)
        sys.exit(0)  

    def partialFactoryReset(self):
        loggerINFO("-----############### partialFactoryReset ###############------")
        params.delete_all_keys()
        self.rebootTerminal()

    def fullFactoryReset(self):
        loggerINFO("-----############### fullFactoryReset ###############------")
        display_off()
        params.delete_all_keys()
        os.system("sudo rm -R /home/pi/ras/data")
        time.sleep(1)
        self.rebootTerminal()
   
    
