from odoo.registerNewDevice import registerNewDevice

from common.common import store_factory_settings_in_database
from common.params import Params
import common.constants as co

params = Params(db=co.PARAMS)
params.put("odooConnectedAtLeastOnce","0")

store_factory_settings_in_database()

uuid_ = "ce99ffbd-597d-43ba-a4c5-791fc1885f2a"

odooAddress    = "http://192.168.178.55:8113/iot/"+uuid_+"/configure"

answer = registerNewDevice(odooAddress)

if answer:
    print("there is an answer")
else:
    print("no answer")

print(f"answer - register_new_device_in_Odoo: {answer}")


"""

answer: {
    'host': 'http://lu:9132', 
    'name': '3d91f1cb-e28c-4656-a0ba-c23444b36e35', 
    'outputs': {}, 
    'inputs': {
        'sync_clocking': {
            'serial': 'f4dbec06-d408-492c-88d3-802d1eabb701', 
            'passphrase': 'c9c815fc-dafe-4de7-a64a-616776075865'
            }, 
        'async_clocking': {
            'serial': '1c1555a2-8955-4a05-871d-fae5d25985d7', 
            'passphrase': '0843388c-75ac-4a4d-a0bd-ac064f33e50d'
            }, 
        'get_options': {
            'serial': '5dbdb0f7-f17d-43a5-8d9a-fb39b6697849', 
            'passphrase': '9aa70797-bf73-4c09-87c8-cc21cfcb5dc2'
            }
        }
    }

"""