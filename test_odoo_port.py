from common.connectivity import isIpPortOpen

try:
    odooHost = "donantes.freedoo.es"
    odooPort = 8106
    odoo_port_open = isIpPortOpen((odooHost, odooPort))
except Exception as e:
    print(f"common.connectivity - exception in method isOdooPortOpen: {e}")
    odoo_port_open = False
print(f"odooPortOpen: {odoo_port_open}")