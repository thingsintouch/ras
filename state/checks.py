import os
from os.path import isfile, join, exists
import time
import sys
import fcntl

from display.helpers import sh1106

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from common.constants import (
    WORKING_DIR, PARAMS, CLOCKINGS, LAST_REGISTERED, TO_BE_DELETED, FILE_ETH0_CONF, FILE_WPA_SUPP_CONF)

from common.params import Params
from odoo.odooRequests import check_if_registered
from common.connectivity import isPingable
from common.common import (
    setTimeZone, reboot, use_self_generated_eth0_MAC_address, 
    on_ethernet, read_wifi_credentials, write_to_file,
    send_email, delete_file, create_file, get_network_info)
from factory_settings.custom_params import factory_settings



params = Params(db=PARAMS)

list_of_boolean_flags = [
    "shouldGetFirmwareUpdate",
    "rebootTerminal",
    "partialFactoryReset",
    "fullFactoryReset",
    "shutdownTerminal",
    "deleteClockings",
    "setEthernetMAC",
    "send_emailLogs",
    "marry_router",
    "divorce_router"
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
        self.action_for_boolean_flag = {
            "shouldGetFirmwareUpdate"   : self.shouldGetFirmwareUpdate,
            "shutdownTerminal"          : self.shutdownTerminal,
            "rebootTerminal"            : self.rebootTerminal,
            "partialFactoryReset"       : self.partialFactoryReset,
            "fullFactoryReset"          : self.fullFactoryReset,
            "deleteClockings"           : self.deleteClockings,
            "setEthernetMAC"            : self.setEthernetMAC,
            "deleteIPs"                 : self.deleteIPs,
            "send_emailLogs"            : self.send_emailLogs,
            "marry_router"              : self.marry_router,
            "divorce_router"            : self.divorce_router,
        }

    def check_and_execute(self):
        self.check_if_registered_once_after_every_launch()
        for boolean_flag in list_of_boolean_flags:
            if params.get(boolean_flag) == "1":
                set_all_boolean_flags_to_false()
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
        display_off()
        loggerINFO("-----############### fullFactoryReset ###############------")
        params.delete_all_keys()
        os.system("sudo sh /home/pi/ras/state/fullFactoryReset.sh")
        time.sleep(60)
        sys.exit(0)

    def deleteClockings(self):
        loggerINFO("-----############### deleteClockings stored in the device (locally) ###############------")
        file_path ="still not defined"
        try:
            for f in os.listdir(CLOCKINGS):
                if isfile(join(CLOCKINGS, f)):
                    file_path = join(CLOCKINGS, f)
                    delete_file(file_path)
                    if exists(file_path):
                        create_file(TO_BE_DELETED, f)
            time.sleep(0.2)
        except Exception as e:
            loggerINFO(f"there was an Exception while trying to delete the clockings files: {e} - file_path was: {file_path}")

    def check_daily_reboot(self):
        current_time =  time.localtime()
        current_minute = time.strftime("%M", current_time)
        # print(f" check_daily_reboot - current_minute {current_minute} ")
        if current_minute == params.get("dailyRebootMinute"):
            current_hour = time.strftime("%H", current_time) 
            if current_hour == params.get("dailyRebootHour"):
                if params.get("automaticUpdate") == "1":
                    self.shouldGetFirmwareUpdate()
                else:
                    #time.sleep(10) # avoid to reboot twice
                    self.rebootTerminal()
    
    def setEthernetMAC(self):
        loggerINFO("-----############### set unique Ethernet MAC ###############------")
        use_self_generated_eth0_MAC_address()
    
    def deleteIPs(self):
        loggerINFO("-----############### delete all IPs on wlan0 and etho ###############------")
        os.system("sudo ip addr flush eth0")
        os.system("sudo ip addr flush wlan0")

    def send_emailLogs(self):
        loggerINFO("-----############### send email Logs ###############------")
        try:
            email = params.get("emailLogs") or False
            serial_number = factory_settings["productionNumber"] or "no s/n"
            subject = f"RAS #{serial_number} - log of last registered cards"
            if email:
                send_email(email, subject, "Please find attached the last 500 registered cards. \n\n", LAST_REGISTERED)
        except:
            pass
    
    def marry_router(self):
        loggerINFO("-----############### Associate current router permanently to the device ###############------")
        network = get_network_info()
        # wlan0_router_MAC_address = network["wlan0"]["mac_router"] or "N/A"
        # wlan0_router_ip = network["wlan0"]["ip_router"] or "N/A"
        # wlan0_device_ip = network["wlan0"]["ip_device"] or "N/A"
        if network["eth0"]["ip_device"] and network["eth0"]["mac_router"]:
            content_eth0_conf = \
                "allow-hotplug eth0"+"\n"+ \
                "iface eth0 inet dhcp"+"\n"+ \
                "    hwaddress ether "+ network["eth0"]["mac_router"]
            write_to_file(filename=FILE_ETH0_CONF, content=content_eth0_conf)
        if network["wlan0"]["ip_device"] and network["wlan0"]["mac_router"]:
            ssid, psk = read_wifi_credentials()
            if ssid and psk:
                content_wpa_conf = \
                    "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"+"\n"+ \
                    "update_config=1"+"\n"+ \
                    "\n"+ \
                    "network={ \n" + "    ssid=\""+ ssid + "\"\n"+ \
                    "    psk=\""+ psk + "\"\n"+ \
                    "    bssid="+ network["wlan0"]["mac_router"] + "\"\n"+ \
                    "}\n"
                write_to_file(filename=FILE_WPA_SUPP_CONF, content=content_wpa_conf)   
        print("sudo service networking restart")      

    def divorce_router(self):
        loggerINFO("-----############### Remove any association to a specific router ###############------")
        delete_file(FILE_ETH0_CONF)
        
class Timezone_Checker():

    def __init__(self):
        self.timezone_current = params.get("tz")
    
    def check_and_set(self):
        timezone_now = params.get("tz") 
        if timezone_now != self.timezone_current:
           setTimeZone(tz= timezone_now) 
           self.timezone_current = timezone_now

   

