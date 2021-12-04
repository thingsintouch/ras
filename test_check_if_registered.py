from odoo.odooRequests import check_if_registered

template    = "http://lu:9131"
serial      = "b41dc469-385e-4c68-bcd5-cb85ce7b4606"
passphrase  = "08b5e8e0-56b7-48c4-b03c-555c539e829a"

registered = check_if_registered(template, serial, passphrase)

print(f"registered (state): {registered}")