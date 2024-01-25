from common.connectivity import isIpPortOpen

# odooHost = params.get("odoo_host")
# odooPort = params.get("odoo_port")

odooHost =""
odooPort=int("443")

ipPort = (odooHost, odooPort)

print(f"isIpPortOpen {isIpPortOpen(ipPort)}")