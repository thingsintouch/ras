import time

from os import listdir, remove
from os.path import isfile, join

from common.logger import loggerDEBUG, loggerINFO
import common.constants as co
import common.common as cc

from common.constants import PARAMS, CLOCKINGS, SECONDS_UNTIL_CLOCKINGS_DELETED_LOCALLY
from common.params import Params
from common.keys import TxType, keys_by_Type

from odoo.odooRequests import postToOdooRegisterClockings



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

def registerClockings():
    if params.get("odooPortOpen") == "1":
        once_at_a_time_register_clockings()
   