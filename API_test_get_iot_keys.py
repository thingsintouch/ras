from odoo.get_iot_keys import get_iot_keys
from common.common import pPrint
from common.connectivity import isOdooPortOpen
from common.params import Params
import common.constants as co

params = Params(db=co.PARAMS)

if isOdooPortOpen():

    serial_of_input = str(params.get("serial_call_lock_sync"))
    type_of_key = "RFID"
    answer = get_iot_keys(serial_of_input, type_of_key)

    print(f"full answer:")
    pPrint(answer)

else:
    print("odoo port closed")