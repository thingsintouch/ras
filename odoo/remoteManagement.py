from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from common.common import pPrint, setTimeZone

import common.logger as lo
from common.constants import PARAMS, ROUTE_ACK_GATE
from common.params import Params, Log
from common.keys import TxType
from odoo.odooRequests import post_request_and_get_answer

params = Params(db=PARAMS)
log_db =  Log()

def getPayload(settings_to_send):
    payload = {}
    inc_log = log_db.get_whole_log()
    params.put('incrementalLog', inc_log)
    for s in settings_to_send:
        try:
            payload[s] = params.get(s)
        except Exception as e:
            loggerERROR(f"Exception while trying to access setting {s}")
    #pPrint(payload)
    return payload

def acknowledgeTerminalInOdoo():
    template = params.get("odooUrlTemplate")
    if template is None: return False

    loggerDEBUG(f"Trying to get ACK from Odoo {template}, ROUTE_ACK_GATE {ROUTE_ACK_GATE} ")
    requestURL  = template + ROUTE_ACK_GATE   
    payload     = getPayload(params.get_list_of_all_keys())
    answer = post_request_and_get_answer(requestURL, payload)

    if answer:
        error = answer.get("error", None)
        if error:
            loggerDEBUG(f"Could not acknowledge the terminal in Odoo- error: {error}")
        else:
            list_on_ack_from_odoo = params.get_list_of_keys_with_type(TxType.ON_ACK_FROM_ODOO)
            for o in list_on_ack_from_odoo:
                value = answer.get(o, False)
                loggerDEBUG(f"key: {o}; value:{value} ") 
                if type(value) != bool : value = str(value)
                params.put(o,value)
            if answer["tz"]:
                loggerDEBUG(f"setting time zone to {answer['tz']}")
                setTimeZone()
            loggerINFO(f"****************** Terminal acknowledged in Odoo ***************")
            params.put("acknowledged", True)
    else:
        loggerINFO(f"Answer from Odoo did not contain an answer")
