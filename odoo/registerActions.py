from os import listdir, remove
from os.path import isfile, join

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import call_lock_async

from common.constants import PARAMS, KEY_ACTIONS
from common.params import Params

params = Params(db=PARAMS)

def get_sorted_actions_from_older_to_newer():
    action_tuples = []
    for f in listdir(KEY_ACTIONS):
        if isfile(join(KEY_ACTIONS, f)):
            splitted  = f.split("-")
            card_code = splitted[0]
            f_end = splitted[1]
            splitted_end = f_end.split("%")
            timestamp = splitted_end[0]
            if splitted_end[1] == "1":
                state = "ON"
            else:
                state="OFF"
            action_tuples.append((timestamp, card_code, state, f))
    return sorted(action_tuples, key=lambda action: action[0])
             

def registerActions():
    if params.get("odooPortOpen") == "1":
        card_codes_to_not_process   = []
        sorted_action_tuples = get_sorted_actions_from_older_to_newer()
        loggerDEBUG(f"sorted_action_tuples {sorted_action_tuples}")
        for action_tuple in sorted_action_tuples:
            loggerDEBUG(f"processing action {action_tuple}")
            card_code = action_tuple[1]
            if card_code not in card_codes_to_not_process:
                try:
                    action_file = action_tuple[3]
                    timestamp = action_tuple[0]
                    state = action_tuple[2]
                    answer = call_lock_async(card_code, timestamp, state)
                except Exception as e:
                    loggerDEBUG(f"Could not Register action {action_file} - Exception: {e}")
                    answer = False
                if answer:
                    if answer.get("status", False) and answer.get("status") == "ok":
                        remove(join(KEY_ACTIONS,action_file))
                    else: # do not process all the older actions if a action for a card has failed
                        card_codes_to_not_process.append(card_code) 