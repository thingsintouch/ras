from odoo.odooRequests import register_new_device_in_Odoo
from common.connectivity import extract_odoo_host_and_port

from common.keys import TxType, keys_by_Type

from common.constants import PARAMS
from common.params import Params

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

params = Params(db=PARAMS)

def parameters_to_send_on_registering():
    to_send = {}
    keys_to_be_sent =  keys_by_Type[TxType.ON_REGISTERING_FROM_DEVICE]
    for k in keys_to_be_sent:
        to_send[k] = params.get(k)
    return to_send

def save_parameters_for_new_device(answer):
    try:
        params.put("RASxxx", answer["name"][:13]) # display only the first characters

        params.put("odooUrlTemplate",   answer["host"])
        extract_odoo_host_and_port()

        params.put("serial_sync",       answer["inputs"]["sync_clocking"]["serial"])
        params.put("passphrase_sync",   answer["inputs"]["sync_clocking"]["passphrase"])

        params.put("serial_async",      answer["inputs"]["async_clocking"]["serial"])
        params.put("passphrase_async",  answer["inputs"]["async_clocking"]["passphrase"])

        params.put("serial_routine",      answer["inputs"]["get_options"]["serial"])
        params.put("passphrase_routine",  answer["inputs"]["get_options"]["passphrase"])        

        params.put("odooConnectedAtLeastOnce", "1")
        return True
    except Exception as e:
        loggerDEBUG(f"save_parameters_for_new_device - Exception: {e}")
    return False

def registerNewDevice(odooAddress):
    answer = register_new_device_in_Odoo(odooAddress, parameters_to_send_on_registering())
    if answer:
        result = save_parameters_for_new_device(answer)
        return result
    else:
        return False