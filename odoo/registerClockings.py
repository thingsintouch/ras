import requests
import json
import time

from os import listdir, remove
from os.path import isfile, join

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
import common.constants as co
import common.common as cc

from common.constants import PARAMS, CLOCKINGS, SECONDS_UNTIL_CLOCKINGS_DELETED_LOCALLY
from common.params import Params
from common.keys import TxType, keys_by_Type



params              = Params(db=PARAMS)

productName         = params.get('productName')

def getClockings():
    clockings = []
    NOW_in_seconds = int(time.time())
    limit_for_clockings_to_remain = NOW_in_seconds - SECONDS_UNTIL_CLOCKINGS_DELETED_LOCALLY
    for f in listdir(CLOCKINGS):
        if isfile(join(CLOCKINGS, f)):
            [card, timestamp_in_seconds] = f.split('-')
            if int(timestamp_in_seconds) < limit_for_clockings_to_remain:
                remove(join(CLOCKINGS,f))
                loggerINFO(f"removed old clocking stored locally: {f}")
            else:
                clockings.append(f) 
    return clockings

def postToOdooRegisterClockings(clockings):
    try:
        requestURL  = params.get("odooUrlTemplate") +  co.ROUTE_INCOMING_IN_ODOO + \
                      "/" + params.get("routefromDeviceToOdoo")
        headers     = {'Content-Type': 'application/json'}
        # loggerDEBUG(f"#####################--------------##############")
        # cc.pPrint(clockings)
        # loggerDEBUG(f"#####################--------------##############")
        payload     = {
                    'question'      : co.QUESTION_ASK_FOR_REGISTER_CLOCKINGS,
                    'productName'   : productName,
                    'clockings'     : clockings
                    }
        response    = requests.post(url=requestURL, json=payload, headers=headers, verify=False)
        answer      = response.json().get("result", False)
        #loggerDEBUG(f"REGISTER CLOCKINGS answer: {answer}")
        return  answer
    except ConnectionRefusedError as e:
        loggerDEBUG(f"Register Clockings not Available - ConnectionRefusedError - Request Exception : {e}")
        return False
    except Exception as e:
        loggerDEBUG(f"Register Clockings not Available - Exception: {e}")
        return False

def process_answer_from_register_clockings(answer):
    if not answer:
        loggerDEBUG(f"Register Clockings not Available - No Answer from Odoo") 
    else:    
        error = answer.get("error", False)
        if error:
            loggerDEBUG(f"Register Clockings not Available - error in answer from Odoo: {error}")
        else:
            loggerDEBUG(f"Register Clockings done - no error") 
            processed_clockings = answer.get("processed_clockings", False)
            if processed_clockings:
                for c in processed_clockings:
                    remove(join(CLOCKINGS,c))

def once_at_a_time_register_clockings():
    for clocking in getClockings():
        clockings = []
        clockings.append(clocking)
        answer = postToOdooRegisterClockings(clockings)
        process_answer_from_register_clockings(answer)

# def all_at_once_register_clockings():
#     answer = postToOdooRegisterClockings(getClockings())
#     process_answer_from_register_clockings(answer)

def registerClockings():
    once_at_a_time_register_clockings() # alternatively all_at_once_register_clockings
    


