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
        if check_if_registered():
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
