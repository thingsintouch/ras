from time import sleep

from odooGetIotKeys.stored_keys import Stored_keys, update_stored_keys

from common.common import get_period
from common.common import BLOCKING_waiting_until_RAS_acknowledged_from_Odoo


stored_keys = Stored_keys()

def main():

    BLOCKING_waiting_until_RAS_acknowledged_from_Odoo()

    while True:
        update_stored_keys(stored_keys)
        sleep(get_period("period_odoo_get_iot_keys"))

if __name__ == "__main__":
    main()
