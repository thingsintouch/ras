import time

from common import constants as co
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.params import Params
from display.helpers import Oled
from common.connectivity import extract_odoo_host_and_port 

from odoo.registerNewDevice import registerNewDevice
from buzzer.helpers import buzz

params = Params(db=co.PARAMS)
oled = Oled()

def main(odooAddress):
    buzz("OK")
    params.put("displayClock", "no")
    text = f"CONNECTING\nWITH ODOO\n{odooAddress}"
    oled.three_lines_text_small(text)
    loggerINFO(f"connect_To_Odoo main - odooAddress:{odooAddress}")
    if registerNewDevice(odooAddress):
        extract_odoo_host_and_port()
        text = f"SUCCESSFULLY\nCONNECTED WITH ODOO\n{odooAddress}"
        loggerINFO(f"Connected with Odoo: {odooAddress}")
        buzz("success_odoo_connection")
        registration_result = True
    else:
        text = f"NO CONNECTION\nPOSSIBLE\n{odooAddress}"
        loggerINFO(f"NO CONNECTION WITH ADDRESS {odooAddress}")
        buzz("failed_odoo_connection")
        registration_result = False
      
    oled.three_lines_text_small(text)
    time.sleep(4)
    params.put("displayClock", "yes")
    return registration_result

if __name__ == "__main__":
    main()
