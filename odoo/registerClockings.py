import time

from os import listdir, remove
from os.path import isfile, join, exists

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import register_async_clocking

from common.constants import PARAMS, CLOCKINGS, IN_OR_OUT, TO_BE_DELETED
from common.params import Params
from common.common import write_to_file, get_timestamp_human, delete_file

params = Params(db=PARAMS)

def set_for_deletion(f):
    if exists(join(TO_BE_DELETED,f)):
        delete_file(join(CLOCKINGS,f))
        if not exists(join(CLOCKINGS,f)):
            delete_file(join(TO_BE_DELETED,f))
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
                try:
                    if int(timestamp) < limit_for_clockings_to_remain:
                        delete_file(join(CLOCKINGS,f))
                        loggerINFO(f"removed old clocking stored locally: {f}")
                    else:
                        clocking_tuples.append((timestamp, card_code, f))
                except Exception as e:
                    loggerINFO(f"could not process {f} on get_sorted_clockings - Exception was {e}")
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
        loggerDEBUG(f"number of sorted_clocking_tuples to be processed {len(sorted_clocking_tuples)}")
        for clocking_tuple in sorted_clocking_tuples:
            [timestamp, card_code, card_code_and_timestamp] = clocking_tuple
            timestamp_human = get_timestamp_human(timestamp_int = timestamp)
            loggerDEBUG(f"processing clocking on {timestamp_human} for card code {card_code}")
            if card_code not in card_codes_to_not_process:
                clocking_info = f"clocking: {timestamp_human} for card {card_code} - "
                message = clocking_info
                try:
                    answer = register_async_clocking(card_code, timestamp)
                except Exception as e:
                    message = clocking_info + f"Could not Register Clocking - Exception: {str(e)}"
                    answer = False
                if answer:
                    employee_name = answer.get("employee_name","")
                    store_name_for_a_rfid_code(card_code, employee_name)
                    params.put("lastConnectionWithOdoo", time.strftime("%d-%b-%Y %H:%M", time.localtime()))
                    loggerDEBUG(f"full answer from Odoo {answer}")
                    if answer.get("logged", False):
                        message = clocking_info + f"{employee_name} logged in Odoo"
                        in_or_out = answer.get("action", "no action")
                        write_to_file(join(IN_OR_OUT,card_code),in_or_out + "\n")
                        delete_file(join(CLOCKINGS,card_code_and_timestamp))
                    else: # do not process all the older clockings if a clocking for a card has failed
                        error_message = answer.get("error_message", "No error message received.")
                        delete_not_recognized_cards = params.get("delete_clockings_not_recognized") is not None and params.get("delete_clockings_not_recognized")=="1"
                        message = clocking_info + f"{employee_name} not logged in Odoo. Error Message from Odoo: {error_message}"
                        if delete_not_recognized_cards and q in error_message:
                            delete_file(join(CLOCKINGS,card_code_and_timestamp))
                        else:
                            card_codes_to_not_process.append(card_code)
                else:
                    message = clocking_info + "no answer from Odoo - Odoo could not store this clocking"
                    card_codes_to_not_process.append(card_code)
                if exists(join(CLOCKINGS,card_code_and_timestamp)): write_to_file(join(CLOCKINGS,card_code_and_timestamp), message + "\n")
                loggerINFO(message)
                time.sleep(2)
