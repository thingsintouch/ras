import time
import psutil
import zmq

from common import constants as co
# from connectivity import helpers as ch   # connectivity helpers
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG
from messaging.messaging import PublisherMultipart as Publisher
from common.connectivity import internetReachable, isOdooPortOpen
from common.params import Params
from odoo.odooRequests import check_if_registered


params = Params(db=co.PARAMS)

def check_if_registered_once_after_every_launch():
    if params.get("acknowledged") != "1":
        template        = params.get("odooUrlTemplate")
        serial_rfid     = params.get("serial_sync")
        passphrase_rfid = params.get("passphrase_sync")
        loggerDEBUG(f" checking if the terminal is acknowlegeable by Odoo - once after every launch")
        if check_if_registered(template, serial_rfid, passphrase_rfid):
            params.put("acknowledged", "1")

def main():
    #params.put("acknowledged", "0") # terminal is NOT acknowledged at the beginning # already @ begin of launcher.py

    while True:
        check_if_registered_once_after_every_launch()

        internet_reachable  = internetReachable()
        odoo_port_open      = isOdooPortOpen()
        loggerDEBUG(f"internet pingable {internet_reachable} - odoo port open {odoo_port_open}")
        time.sleep(co.PERIOD_STATE_MANAGER)


if __name__ == "__main__":
    main()
