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
        # template_from_odoo = answer["host"]
        # if "localhost" not in template_from_odoo:
        #     extract_odoo_host_and_port(template_from_odoo)

        params.put("RASxxx", answer.get("name")[:13] or "no name") # display only the first characters

        inputs_list = [
            ("sync", "sync_clocking"),
            ("async", "async_clocking"),
            ("routine", "get_options"),
            ("call_lock_sync", "call_lock_sync"),
            ("call_lock_async", "call_lock_async"),
            ("get_iot_keys", "get_iot_keys")
            ]

        for input_endpoint in inputs_list:
            input_ras_suffix = input_endpoint[0]
            input_db_name = input_endpoint[1]
            loggerDEBUG(f"input_ras_suffix: {input_ras_suffix}, input_db_name: {input_db_name}")
            input_data =  answer["inputs"].get(input_db_name) or False
            if input_data:
                params.put("serial_"+input_endpoint[0], input_data.get("serial"))
                params.put("passphrase_"+input_endpoint[0], input_data.get("passphrase"))
                loggerDEBUG(f"serial_{input_endpoint[0]}: {input_data.get('serial')}")
                loggerDEBUG(f"passphrase_{input_endpoint[0]}: {input_data.get('passphrase')}")
        # params.put("serial_async",      answer["inputs"]["async_clocking"]["serial"])
        # params.put("passphrase_async",  answer["inputs"]["async_clocking"]["passphrase"])

        # params.put("serial_routine",      answer["inputs"]["get_options"]["serial"])
        # params.put("passphrase_routine",  answer["inputs"]["get_options"]["passphrase"])        

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