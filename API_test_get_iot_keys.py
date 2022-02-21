from odoo.get_iot_keys import get_iot_keys
from common.common import pPrint
from common.connectivity import isOdooPortOpen

if isOdooPortOpen():

    answer = get_iot_keys()

    print(f"full answer:")
    pPrint(answer)

else:
    print("odoo port closed")