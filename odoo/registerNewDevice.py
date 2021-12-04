from odoo.odooRequests import register_new_device_in_Odoo
from common.connectivity import extract_odoo_host_and_port

from common.constants import PARAMS
from common.params import Params

params              = Params(db=PARAMS)

def save_parameters_for_new_device(answer):
    try:
        params.put("odooUrlTemplate",   answer["host"])
        extract_odoo_host_and_port()
        params.put("serial_sync",       answer["inputs"]["sync_clocking"]["serial"])
        params.put("passphrase_sync",   answer["inputs"]["sync_clocking"]["passphrase"])
        params.put("serial_async",      answer["inputs"]["async_clocking"]["serial"])
        params.put("passphrase_async",  answer["inputs"]["async_clocking"]["passphrase"])
        return True
    except Exception as e:
        loggerDEBUG(f"save_parameters_for_new_device - Exception: {e}")
    return False

def registerNewDevice(odooAddress):
    answer = register_new_device_in_Odoo(odooAddress)
    if answer:
        result = save_parameters_for_new_device(answer)
        return result
    else:
        return False