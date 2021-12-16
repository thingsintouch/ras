from odoo.odooRequests import register_async_clocking

from common.common import runShellCommand_and_returnOutput

timestamp = runShellCommand_and_returnOutput("date +%s").replace("\n","")
card_code = "b75e905f"
#card_code_and_timestamp = card_code + "-" + timestamp

answer = register_async_clocking(card_code, timestamp)

registered = answer.get("logged", False)

print(f"clocking registered (state): {registered}")
print(f"full answer {answer}")