from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.constants import PARAMS, KEY_ACTIONS, MINIMUM_TIME_BETWEEN_RELAY_SWITCHINGS
from common.params import Params, mkdirs_exists_ok, read_db
from os.path import exists

params = Params(db=PARAMS)

if not exists(KEY_ACTIONS):
    mkdirs_exists_ok(KEY_ACTIONS)

def write_action(card_as_string, NOW_in_seconds, relay_status_after_switching):
    file_name_of_the_action = KEY_ACTIONS + "/" + card_as_string + "-" + str(NOW_in_seconds) + "%" + relay_status_after_switching
    with open(file_name_of_the_action, 'w'): pass

def enough_time_betweeen_switchings(NOW_in_seconds):
    last_action = params.get("last_relay_action")
    if last_action is None:
        return True
    elif (NOW_in_seconds - int(last_action)) > MINIMUM_TIME_BETWEEN_RELAY_SWITCHINGS:
        return True
    else:
        return False

def switch_the_relay():
    status_relay_before = params.get("relay_status")
    if status_relay_before is None:
        status_relay_before = "0"
    if status_relay_before == "0":
        params.put("relay_status", "1")
        return "1"
    else:
        params.put("relay_status", "0")
        return "0"

def switch_the_relay_after_checks(card_as_string, NOW_in_seconds):

    if enough_time_betweeen_switchings(NOW_in_seconds):
        relay_status_after_switching = switch_the_relay()
        write_action(card_as_string, NOW_in_seconds, relay_status_after_switching)

        loggerINFO(f"##########################################################")
        loggerINFO(f"card {card_as_string} - relay_status_after_switching {relay_status_after_switching}")
        loggerINFO(f"##########################################################")