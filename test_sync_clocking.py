from odoo.odooRequests import register_sync_clocking

rfid_card_code  = "b75e905f"

answer = register_sync_clocking(rfid_card_code)

registered = answer.get("logged", False)

print(f"clocking registered (state): {registered}")
print(f"full answer {answer}")