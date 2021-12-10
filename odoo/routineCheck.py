from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import routine_check

from common.constants import PARAMS
from common.params import Params, Log
from common.keys import TxType, keys_by_Type

params              = Params(db=PARAMS)

keys_to_be_saved =  keys_by_Type[TxType.ON_ROUTINE_CALLS] + keys_by_Type[TxType.DISPLAY_MESSAGE]
# cc.pPrint(keys_to_be_saved)
productName = params.get('productName')

list_of_boolean_flags = [
    "shouldGetFirmwareUpdate",
    "rebootTerminal",
    "partialFactoryReset",
    "fullFactoryReset",
    "shutdownTerminal",
]

def routineCheck():
    to_send = {
        "param 1": "value 1",
        "param 2": "value 2",
        }

    answer = routine_check(to_send)

    if answer:
        error = answer.get("error", False)
        if error:
            loggerDEBUG(f"Routine Check not Available - error in answer from Odoo: {error}")
        else:
            loggerDEBUG(f"Routine Check done - no error - {answer}") # {answer}
            params.put("isRemoteOdooControlAvailable", "1")
            saveChangesToParams(answer)
            return True
    else:
        loggerDEBUG(f"Routine Check not Available - No Answer from Odoo")        

    params.put("isRemoteOdooControlAvailable", False)
    return False

def saveChangesToParams(answer):
    for k in answer:
        ans = answer.get(k, None)
        if ans is not None:
            if ans is False: ans = "0"
            if ans is True : ans = "1"
            if k in keys_to_be_saved:
                ans = str(ans)
                if ans != params.get(k):
                    if k in list_of_boolean_flags:
                        if ans == "1":
                            loggerDEBUG(f"from routine check - storing {k}: {ans}")
                            params.put(k,ans)
                    else:
                        loggerDEBUG(f"from routine check - storing {k}: {ans}")
                        params.put(k,ans)                       
            elif k == "rfid_codes_to_names":
                for code in ans:
                    if code in params.keys:
                        if ans[code] != params.get(code):
                            loggerDEBUG(f"from routine check - storing {code}: {ans[code]}")
                            params.put(code,ans[code])
                    else:
                        params.add_rfid_card_code_to_keys(code)
                        loggerDEBUG(f"from routine check - CREATED and storing {code}: {ans[code]}")
                        loggerDEBUG(f"params.keys {params.keys}")
                        params.put(code,ans[code])                        
            else:
                loggerDEBUG(f"this key in answer from routine call is NOT STORED {k}: {ans}")
