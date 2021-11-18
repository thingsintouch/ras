
#odooAddress = params.get("odooUrlTemplate")
odooAddress = "https://example.com:443"
odooAdressSplitted = odooAddress.split(":")
length = len(odooAdressSplitted)
print(f"odooAdressSplitted {odooAdressSplitted} - length {length}")

if length == 1:
    print("odoo_host:", odooAdressSplitted[0])
    print("odoo_port", "443")
if length == 2:
    zero = odooAdressSplitted[0]
    one = odooAdressSplitted[1]
    if zero == "https":
        print("odoo_host", one)
        print("odoo_port","443")
    else:
        print("odoo_host", zero)
        print("odoo_port", one)
if length == 3:
    if "//" in odooAdressSplitted[1]:
        odoo_host = odooAdressSplitted[1].replace('/','')
        print("odoo_host", odoo_host)
        print("odoo_port", odooAdressSplitted[2])
    else:
        print("odoo_host", "0")
        print("odoo_port", "0")
# odooHost = params.get("odoo_host")
# odooPort = params.get("odoo_port")
# print(f"odoo_host {odooHost}- odoo_port {odooPort}")