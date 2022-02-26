from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import request_get_iot_keys

from common.constants import PARAMS
from common.params import Params
from common.keys import TxType, keys_by_Type
from common.common import pPrint

params  = Params(db=PARAMS)


def get_iot_keys_from_odoo(serial_of_input, type_of_key):
    to_send = {
        "serial_of_input" : serial_of_input,
        "type_of_key" : type_of_key,
        }

    answer = request_get_iot_keys(to_send)

    if answer:
        error = answer.get("error", False)
        if error:
            loggerDEBUG(f"get_iot_keys not Available - error in answer from Odoo: {error}")
        else:
            loggerDEBUG(f"get_iot_keys done - no error - {answer}") # {answer}
            # pPrint(answer)
            params.put("isRemoteOdooControlAvailable", "1")
            keys = answer.get("keys", False)
            if keys:
                return keys
    else:
        loggerDEBUG(f"get_iot_keys not Available - No Answer from Odoo")        

    params.put("isRemoteOdooControlAvailable", False)
    return False
