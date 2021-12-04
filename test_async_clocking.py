from odoo.odooRequests import register_async_clocking

template        = "http://lu:9131"
serial      = "b41dc469-385e-4c68-bcd5-cb85ce7b4606"
passphrase  = "08b5e8e0-56b7-48c4-b03c-555c539e829a"
card_code_and_timestamp  = "b75e905f-1638639830"

answer = register_async_clocking(template, serial, passphrase, card_code_and_timestamp)

registered = answer.get("logged", False)

print(f"clocking registered (state): {registered}")