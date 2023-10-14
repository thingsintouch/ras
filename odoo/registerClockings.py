import time

from os import listdir, remove
from os.path import isfile, join, exists

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import register_async_clocking

from common.constants import PARAMS, CLOCKINGS, IN_OR_OUT, TO_BE_DELETED
from common.params import Params
from common.common import write_to_file

params = Params(db=PARAMS)

def set_for_deletion(f):
    if exists(join(TO_BE_DELETED,f)):
        remove(join(CLOCKINGS,f))
        if not exists(join(CLOCKINGS,f)):
            remove(join(TO_BE_DELETED,f))
        return True
    else:
        return False

def get_sorted_clockings_from_older_to_newer():
    clocking_tuples = []
    now_in_seconds = int(time.time())
    expiration_period_in_weeks = params.get("clockings_expiration_period_in_weeks") or "2"
    seconds_until_clockings_deleted_locally = int(expiration_period_in_weeks)*7*24*60*60
    limit_for_clockings_to_remain = now_in_seconds - seconds_until_clockings_deleted_locally
    for f in listdir(CLOCKINGS):
        if isfile(join(CLOCKINGS, f)):
            if not set_for_deletion(f):
                splitted  = f.split("-")
                card_code = splitted[0]
                timestamp = splitted[1]
                if int(timestamp) < limit_for_clockings_to_remain:
                    remove(join(CLOCKINGS,f))
                    loggerINFO(f"removed old clocking stored locally: {f}")
                else:
                    clocking_tuples.append((timestamp, card_code, f))
    return sorted(clocking_tuples, key=lambda clocking: clocking[0])

def store_name_for_a_rfid_code(code, name):
    if code in params.keys:
        if name != params.get(code):
            loggerDEBUG(f"store_name_for_a_rfid_code - storing {code}: {name}")
            params.put(code,name)
    else:
        params.add_rfid_card_code_to_keys(code)
        loggerDEBUG(f"store_name_for_a_rfid_code - CREATED and storing {code}: {name}")
        #loggerDEBUG(f"params.keys {params.keys}")
        params.put(code,name)                

def registerClockings():
    if params.get("odooPortOpen") == "1":
        card_codes_to_not_process   = []
        sorted_clocking_tuples = get_sorted_clockings_from_older_to_newer()
        loggerDEBUG(f"sorted_clocking_tuples {sorted_clocking_tuples}")
        for clocking_tuple in sorted_clocking_tuples:
            loggerDEBUG(f"processing clocking {clocking_tuple}")
            card_code = clocking_tuple[1]
            if card_code not in card_codes_to_not_process:
                message_to_write_in_file = "Odoo could not store this clocking"
                try:
                    card_code_and_timestamp = clocking_tuple[2]
                    timestamp = clocking_tuple[0]
                    answer = register_async_clocking(card_code, timestamp)
                    time.sleep(3.6)
                except Exception as e:
                    message_to_write_in_file = f"Could not Register Clocking {card_code_and_timestamp} - Exception: {e}"
                    write_to_file(join(CLOCKINGS,card_code_and_timestamp),message_to_write_in_file + "\n")
                    loggerDEBUG(message_to_write_in_file)
                    answer = False
                if answer:
                    loggerDEBUG(f"processing clocking - answer from Odoo {answer} ")
                    employee_name = answer.get("employee_name","")
                    store_name_for_a_rfid_code(card_code, employee_name)
                    params.put("lastConnectionWithOdoo", time.strftime("%d-%b-%Y %H:%M", time.localtime()))
                    if answer.get("logged", False):
                        # params.put("lastConnectionWithOdoo", time.strftime("%d-%b-%Y %H:%M", time.localtime()))
                        loggerINFO(f"clocking logged in Odoo - answer from Odoo {answer} ")
                        in_or_out = answer.get("action", "no action")
                        write_to_file(join(IN_OR_OUT,card_code),in_or_out + "\n")
                        remove(join(CLOCKINGS,card_code_and_timestamp))
                    else: # do not process all the older clockings if a clocking for a card has failed
                        error_message = answer.get("error_message", "No error message received.") 
                        message_to_write_in_file = "Clocking has not been logged in Odoo. Error Message from Odoo: " + error_message
                        write_to_file(join(CLOCKINGS,card_code_and_timestamp), message_to_write_in_file + "\n")
                        card_codes_to_not_process.append(card_code)
                else:
                    write_to_file(join(CLOCKINGS,card_code_and_timestamp), message_to_write_in_file + "\n")
                    card_codes_to_not_process.append(card_code)
