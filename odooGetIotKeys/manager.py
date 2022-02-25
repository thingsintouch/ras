from time import sleep

from odooGetIotKeys.get_iot_keys import get_iot_keys
from odooGetIotKeys.store_iot_keys import make_sure_dir_KEYS_exists

from common.common import get_period
from common.common import BLOCKING_waiting_until_RAS_acknowledged_from_Odoo
from common.constants import PARAMS
from common.params import Params

params = Params(db=PARAMS)

make_sure_dir_KEYS_exists()

def main():

    BLOCKING_waiting_until_RAS_acknowledged_from_Odoo()

    while True:
        serial_of_input = str(params.get("serial_call_lock_sync"))
        type_of_key = "RFID"
        get_iot_keys(serial_of_input, type_of_key)
        sleep(get_period("period_odoo_get_iot_keys"))

if __name__ == "__main__":
    main()
