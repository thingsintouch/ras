from odoo.odooRequests import routine_check

payload = {"value" : "needed"}

answer = routine_check(payload)

print(f"answer - get options: {answer}")