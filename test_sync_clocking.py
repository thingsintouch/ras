from odoo.odooRequests import register_sync_clocking

template        = "http://lu:9131"
serial          = "11af4d5b-fd07-41d7-8d9b-6f82756fb17b"
passphrase      = "091eadbf-27ea-46f6-8c1f-ddb5341c08dc"
rfid_card_code  = "b75e905f"

answer = register_sync_clocking(template, serial, passphrase, rfid_card_code)

registered = answer.get("logged", False)

print(f"clocking registered (state): {registered}")