import time

from common import constants as co
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.params import Params
from display.helpers import Oled

from common.common import runShellCommand_and_returnOutput as rs
from common.connectivity import internetReachable

from buzzer.helpers import buzz

params = Params(db=co.PARAMS)
oled = Oled()

def main(ssidName, ssidPassword):
    buzz("OK")
    params.put("displayClock", "no")
    text = f"CONNECTING\nWITH SSID\n{ssidName}"
    oled.three_lines_text_small(text)
    if " " in ssidName:
        ssidName = "'" + ssidName + "'"
    answer = (rs('sudo nmcli dev wifi con '+ssidName+' password '+ssidPassword))
    if internetReachable():
        buzz("success_odoo_connection")
        text = f"CONNECTED\nWITH THE\nINTERNET"
        loggerINFO(f"Connected to Interned - SSID: {ssidName}")
    else:
        buzz("failed_odoo_connection")
        text = f"NO CONNECTION\nWITH THE\nINTERNET"
    oled.three_lines_text_small(text)
    time.sleep(4) 
    params.put("displayClock", "yes")

if __name__ == "__main__":
    main()
