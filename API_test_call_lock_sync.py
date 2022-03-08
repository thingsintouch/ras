from odoo.odooRequests import call_lock_sync

from common.common import runShellCommand_and_returnOutput

from common.connectivity import isOdooPortOpen

if isOdooPortOpen():
    #timestamp = runShellCommand_and_returnOutput("date +%s").replace("\n","")
    card_code = "9d5e50d3"
    #card_code_and_timestamp = card_code + "-" + timestamp

    answer = call_lock_sync(card_code)

    #registered = answer.get("logged", False)

    #print(f"clocking registered (state): {registered}")
    print(f"full answer {answer}")
else:
    print("odoo port closed")