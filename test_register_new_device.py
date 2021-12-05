from odoo.registerNewDevice import registerNewDevice

odooAddress    = "http://lu:9131/iot/260a/conf"

answer = registerNewDevice(odooAddress)

if answer:
  print("there is an answer")
else:
  print("no answer")

print(f"answer - register_new_device_in_Odoo: {answer}")