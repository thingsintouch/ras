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
    template                    = params.get("odooUrlTemplate")
    serial_async                = params.get("serial_async")
    passphrase_async            = params.get("passphrase_async")
    card_codes_to_not_process   = []

    sorted_clocking_tuples = get_sorted_clockings_from_older_to_newer()
    print(f"sorted_clocking_tuples {sorted_clocking_tuples}")
    for c in sorted_clocking_tuples:
        print(f"processing clocking {c}")
        if c[1] not in card_codes_to_not_process:
            try:
                answer = register_async_clocking(template, serial_async, passphrase_async, c[2])
            except Exception as e:
                loggerDEBUG(f"Could not Register Clocking {c[2]} - Exception: {e}")
                answer = False
            if answer:
                if answer.get("logged", False):
                    remove(join(CLOCKINGS,c[2]))
                    store_name_for_a_rfid_code(c[1], answer.get("employee_name","-"))
                else: # do not process all the older clockings if a clocking for a card has failed
                    card_codes_to_not_process.append(c[1]) 