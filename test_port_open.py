from common.connectivity import isIpPortOpen

odooHost = "xxx"
odooPort = 443

try:
    odoo_port_open = isIpPortOpen((odooHost, odooPort))
except Exception as e:
    odoo_port_open = False
print(f" odoo_port_open -  {odoo_port_open}")