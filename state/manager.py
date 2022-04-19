import time
import psutil
import zmq

from common import constants as co
# from connectivity import helpers as ch   # connectivity helpers
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG
from messaging.messaging import PublisherMultipart as Publisher
from common.connectivity import internetReachable, isOdooPortOpen
from common.params import Params
from odoo.remoteManagement import acknowledgeTerminalInOdoo


params = Params(db=co.PARAMS)

def main():

    params.put("acknowledged", "0") # terminal is NOT acknowledged at the beginning

    while True:
        if params.get("acknowledged") != "1":
            loggerDEBUG(f" checking if the terminal is acknowlegeable by Odoo - once after every launch")
            acknowledgeTerminalInOdoo()

        internet_reachable  = True 
        odoo_port_open      = isOdooPortOpen()
        loggerDEBUG(f"internet pingable {internet_reachable} - odoo port open {odoo_port_open}")
        time.sleep(co.PERIOD_STATE_MANAGER)


if __name__ == "__main__":
    main()
