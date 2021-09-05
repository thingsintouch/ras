import time

from common import constants as co
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.params import Params
from display.helpers import Oled

from odoo.remoteManagement import isRemoteOdooControlAvailable

params = Params(db=co.PARAMS)


def main(odooAddress):

    oled = Oled()
    params.put("odooUrlTemplate", odooAddress)
    odooAddressOK = isRemoteOdooControlAvailable()
    
    params.put("displayClock", "no")
    if odooAddressOK:
        text = f"CONNECTED\nWITH ODOO\n{odooAddress}"
        loggerINFO(f"CONNECTED WITH ODOO: {odooAddress}")
    else:
        text = f"NO CONNECTION\nWITH ADDRESS\n{odooAddress}"
        loggerINFO(f"NO CONNECTION WITH ADDRESS {odooAddress}")           
    oled.three_lines_text(text)
    time.sleep(8)
    params.put("displayClock", "yes")

if __name__ == "__main__":
    main()
