from odoo.routineCheck import routineCheck
from common.common import pPrint
from common.connectivity import isOdooPortOpen

if isOdooPortOpen():

    answer = routineCheck()

    print(f"full answer:")
    pPrint(answer)

else:
    print("odoo port closed")