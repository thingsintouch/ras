from odoo.odooRequests import call_lock_async

from common.common import runShellCommand_and_returnOutput

from common.connectivity import isOdooPortOpen

if isOdooPortOpen():
    timestamp = runShellCommand_and_returnOutput("date +%s").replace("\n","")
    card_code = "4a338f6a"
    #card_code_and_timestamp = card_code + "-" + timestamp
    state = "OFF"

    answer = call_lock_async(card_code, timestamp, state)

    #registered = answer.get("logged", False)

    #print(f"clocking registered (state): {registered}")
    print(f"full answer {answer}")
else:
    print("odoo port closed")