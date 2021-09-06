import time

from common import constants as co
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.params import Params
from display.helpers import Oled
from common.connectivity import extract_odoo_host_and_port 

from odoo.remoteManagement import isRemoteOdooControlAvailable
from buzzer.helpers import buzz

params = Params(db=co.PARAMS)


def main(odooAddress):

    oled = Oled()
    params.put("odooUrlTemplate", odooAddress)
    odooAddressOK = isRemoteOdooControlAvailable()
    
    params.put("displayClock", "no")
    if odooAddressOK:
        extract_odoo_host_and_port()
        text = f"CONNECTED\n\nWITH ODOO"
        loggerINFO(f"CONNECTED WITH ODOO: {odooAddress}")
        buzz("success_odoo_connection")
    else:
        text = f"NO CONNECTION\n\nPOSSIBLE"
        loggerINFO(f"NO CONNECTION WITH ADDRESS {odooAddress}")
        buzz("failed_odoo_connection")          
    oled.three_lines_text(text)
    time.sleep(3)
    params.put("displayClock", "yes")

if __name__ == "__main__":
    main()
