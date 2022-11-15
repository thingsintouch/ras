import os
from os.path import isfile, join
import time
import sys

from display.helpers import sh1106

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from common.constants import WORKING_DIR, PARAMS, CLOCKINGS

from common.params import Params
from odoo.odooRequests import check_if_registered
from common.connectivity import isPingable
from common.common import setTimeZone, reboot


params = Params(db=PARAMS)

list_of_boolean_flags = [
    "shouldGetFirmwareUpdate",
    "rebootTerminal",
    "partialFactoryReset",
    "fullFactoryReset",
    "shutdownTerminal",
    "deleteClockings"
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
        # self.tz = params.get("tz")
        self.action_for_boolean_flag = {
            "shouldGetFirmwareUpdate"   : self.shouldGetFirmwareUpdate,
            "shutdownTerminal"          : self.shutdownTerminal,
            "rebootTerminal"            : self.rebootTerminal,
            "partialFactoryReset"       : self.partialFactoryReset,
            "fullFactoryReset"          : self.fullFactoryReset,
            "deleteClockings"           : self.deleteClockings
        }

    def check_and_execute(self):
        self.check_if_registered_once_after_every_launch()
        for boolean_flag in list_of_boolean_flags:
            if params.get(boolean_flag) == "1":
                set_all_boolean_flags_to_false()
                # display_off()
                loggerINFO("-"*20 + boolean_flag + "#"*20)
                self.action_for_boolean_flag[boolean_flag]()
                time.sleep(2)

    def check_if_registered_once_after_every_launch(self):
        if not self.acknowledged and params.get("odooPortOpen") == "1":
            if check_if_registered():
                params.put("acknowledged", "1")
                self.acknowledged = True

    def shouldGetFirmwareUpdate(self):
        if isPingable("github.com"):
            loggerINFO("<<<<++++++++ Firmware Update +++++++>>>>>>")
            os.chdir(WORKING_DIR)
            os.system("sudo git fetch origin ras_oca")
            os.system("sudo git reset --hard origin/ras_oca")
            os.system("sudo git fetch -f --all --tags")
            time.sleep(1)
            self.rebootTerminal()
        else:
            loggerINFO("Firmware Update not possible: GitHub is down")   

    def shutdownTerminal(self):
        display_off()
        loggerINFO("-----############### shutdownTerminal ###############------")
        os.system("sudo shutdown now")
        time.sleep(60)
        sys.exit(0)

    def rebootTerminal(self):
        display_off()
        loggerINFO("-----############### rebootTerminal ###############------")
        reboot()
        # os.system("sudo reboot")
        # time.sleep(60)
        # sys.exit(0)  

    def partialFactoryReset(self):
        loggerINFO("-----############### partialFactoryReset ###############------")
        params.delete_all_keys_except_RFIDs()
        self.rebootTerminal()

    def fullFactoryReset(self):
        loggerINFO("-----############### fullFactoryReset ###############------")
        params.delete_all_keys()
        os.system("sudo sh /home/pi/ras/state/fullFactoryReset.sh")
        time.sleep(60)
        sys.exit(0)

    def deleteClockings(self):
        loggerINFO("-----############### deleteClockings stored in the device (locally) ###############------")
        try:
            for f in os.listdir(CLOCKINGS):
                if isfile(join(CLOCKINGS, f)):
                    os.remove(join(CLOCKINGS,f))
        except:
            pass
        time.sleep(1)

    def check_daily_reboot(self):
        current_time =  time.localtime()
        current_minute = time.strftime("%M", current_time)
        # print(f" check_daily_reboot - current_minute {current_minute} ")
        if current_minute == params.get("dailyRebootMinute"):
            current_hour = time.strftime("%H", current_time) 
            if current_hour == params.get("dailyRebootHour"):
                if params.get("automaticUpdate") == "1":
                    self.shouldGetFirmwareUpdate()
                self.rebootTerminal()

class Timezone_Checker():

    def __init__(self):
        self.timezone_current = params.get("tz")
    
    def check_and_set(self):
        timezone_now = params.get("tz") 
        if timezone_now != self.timezone_current:
           setTimeZone(tz= timezone_now) 
           self.timezone_current = timezone_now

   

