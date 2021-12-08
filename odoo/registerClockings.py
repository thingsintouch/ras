from os import listdir, remove
from os.path import isfile, join

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import register_async_clocking

from common.constants import PARAMS, CLOCKINGS
from common.params import Params

params              = Params(db=PARAMS)

def get_sorted_clockings_from_older_to_newer():
    clocking_tuples = []
    for f in listdir(CLOCKINGS):
        if isfile(join(CLOCKINGS, f)):
            splitted  = f.split("-")
            card_code = splitted[0]
            timestamp = splitted[1]
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
    card_codes_to_not_process   = []

    sorted_clocking_tuples = get_sorted_clockings_from_older_to_newer()
    loggerDEBUG(f"sorted_clocking_tuples {sorted_clocking_tuples}")
    for clocking_tuple in sorted_clocking_tuples:
        loggerDEBUG(f"processing clocking {clocking_tuple}")
        card_code = c[1]
        if card_code not in card_codes_to_not_process:
            try:
                card_code_and_timestamp = c[2]
                answer = register_async_clocking(card_code_and_timestamp)
            except Exception as e:
                loggerDEBUG(f"Could not Register Clocking {card_code_and_timestamp} - Exception: {e}")
                answer = False
            if answer:
                if answer.get("logged", False):
                    remove(join(CLOCKINGS,card_code_and_timestamp))
                    store_name_for_a_rfid_code(card_code, answer.get("employee_name","-"))
                else: # do not process all the older clockings if a clocking for a card has failed
                    card_codes_to_not_process.append(card_code) 