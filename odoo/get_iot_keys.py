from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import request_get_iot_keys

from common.constants import PARAMS
from common.params import Params
from common.keys import TxType, keys_by_Type
from common.common import pPrint

params              = Params(db=PARAMS)


def get_iot_keys():
    to_send = {
        }

    answer = request_get_iot_keys(to_send)

    if answer:
        error = answer.get("error", False)
        if error:
            loggerDEBUG(f"get_iot_keys not Available - error in answer from Odoo: {error}")
        else:
            loggerDEBUG(f"get_iot_keys done - no error - {answer}") # {answer}
            pPrint(answer)
            params.put("isRemoteOdooControlAvailable", "1")
            saveChanges(answer)
            return True
    else:
        loggerDEBUG(f"get_iot_keys not Available - No Answer from Odoo")        

    params.put("isRemoteOdooControlAvailable", False)
    return False

def saveChanges(answer):
    pass
    
    # for k in answer:
    #     ans = answer.get(k, None)
    #     if ans is not None:
    #         if ans is False: ans = "0"
    #         if ans is True : ans = "1"
    #         if k in keys_to_be_saved:
    #             ans = str(ans)
    #             if ans != params.get(k):
    #                 if k in list_of_boolean_flags:
    #                     if ans == "1":
    #                         loggerDEBUG(f"from routine check - storing {k}: {ans}")
    #                         params.put(k,ans)
    #                 else:
    #                     ans = check_value_on_change(k,ans)
    #                     loggerDEBUG(f"from routine check - storing {k}: {ans}")
    #                     params.put(k,ans)                       
    #         elif k == "rfid_codes_to_names":
    #             for code in ans:
    #                 if code in params.keys:
    #                     if ans[code] != params.get(code):
    #                         loggerDEBUG(f"from routine check - storing {code}: {ans[code]}")
    #                         params.put(code,ans[code])
    #                 else:
    #                     params.add_rfid_card_code_to_keys(code)
    #                     loggerDEBUG(f"from routine check - CREATED and storing {code}: {ans[code]}")
    #                     loggerDEBUG(f"params.keys {params.keys}")
    #                     params.put(code,ans[code])                        
    #         else:
    #             loggerDEBUG(f"this key in answer from routine call is NOT STORED {k}: {ans}")
