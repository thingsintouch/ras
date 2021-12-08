from odoo.odooRequests import check_if_registered

template    = "http://lu:9131"
serial      = "1c2b000a-698a-4ce4-a680-5b95ae771d29"
passphrase  = "916ad7ee-c4b1-470c-be0b-e7989d63a0c6"

registered = check_if_registered()

print(f"registered (state): {registered}")