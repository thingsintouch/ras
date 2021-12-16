from odoo.odooRequests import check_if_registered

registered = check_if_registered()

print(f"registered (state): {registered}")