from os import listdir, remove
from os.path import isfile, join, exists

from common.params import Params, mkdirs_exists_ok
from common.constants import PARAMS, KEYS

from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR

from odooGetIotKeys.get_iot_keys_from_odoo import get_iot_keys_from_odoo

from common.common import pPrint

params = Params(db=PARAMS)

def update_stored_keys(stored_keys):
    serial_of_input = str(params.get("serial_call_lock_async"))
    type_of_key = "RFID"
    keys_in_odoo = get_iot_keys_from_odoo(serial_of_input, type_of_key)
    if keys_in_odoo:
        stored_keys.check_for_changes(keys_in_odoo)

def make_sure_dir_KEYS_exists():
    if not exists(KEYS):
        mkdirs_exists_ok(KEYS)

def extract_code_and_expiration_from_file_name(file_name):
    splitted  = file_name.split("%")
    key_code = splitted[0]
    expiration_date = int(splitted[1])
    return key_code, expiration_date

def get_keys_stored():
    keys_stored = {}
    for f in listdir(KEYS):
        if isfile(join(KEYS, f)):
            key_code, expiration_date = extract_code_and_expiration_from_file_name(f)
            keys_stored[key_code] = (expiration_date, KEYS + "/"+ f)
    return keys_stored

def get_expiration_date(odoo_key):
    expiration_date = odoo_key.get("expiration_date", False)
    if not expiration_date:
        expiration_date = 0
    return expiration_date

def calculate_file_name(odoo_key):
    return KEYS + "/" + str(odoo_key["unique_virtual_key"]) + "%" + str(get_expiration_date(odoo_key))

class Stored_keys():

    def __init__(self):
        make_sure_dir_KEYS_exists()
        self.keys_stored = get_keys_stored()
        pPrint(self.keys_stored)

    def check_for_changes(self, keys_in_odoo):

        def get_list_of_odoo_keys(keys_in_odoo):
            list_of_odoo_keys = []
            for odoo_key in keys_in_odoo:
                list_of_odoo_keys.append(odoo_key["unique_virtual_key"])
            return list_of_odoo_keys

        def check_for_new_keys_from_odoo(keys_in_odoo):
            for odoo_key in keys_in_odoo:
                if odoo_key["unique_virtual_key"] not in self.keys_stored:
                    self.store_key(odoo_key)

        def check_if_expirations_dates_changed(keys_in_odoo):            
            for odoo_key in keys_in_odoo:
                stored_key = self.keys_stored.get(odoo_key["unique_virtual_key"])
                stored_expiration_date = stored_key[0]
                if get_expiration_date(odoo_key) != stored_expiration_date:
                    print(f"exp date / in odoo {get_expiration_date(odoo_key)} - in store {stored_expiration_date} ")
                    self.remove_key(odoo_key["unique_virtual_key"], stored_key[1])
                    self.store_key(odoo_key)

        def check_if_keys_were_removed(keys_in_odoo, list_of_odoo_keys):
            list_of_stored_keys = list(self.keys_stored.keys())
            pPrint(list_of_stored_keys)
            pPrint(list_of_odoo_keys)
            for key_code in list_of_stored_keys:
                file_name = self.keys_stored[key_code][1]                
                if key_code not in list_of_odoo_keys:
                    self.remove_key(key_code, file_name)

        list_of_odoo_keys = get_list_of_odoo_keys(keys_in_odoo)
        check_for_new_keys_from_odoo(keys_in_odoo)
        check_if_expirations_dates_changed(keys_in_odoo)
        check_if_keys_were_removed(keys_in_odoo, list_of_odoo_keys)


    def store_key(self, odoo_key):
        file_name_of_the_key = calculate_file_name(odoo_key)
        with open(file_name_of_the_key, 'w'): pass
        self.keys_stored[odoo_key["unique_virtual_key"]] = (get_expiration_date(odoo_key), file_name_of_the_key)
        loggerINFO(f"stored a new key with filename: {file_name_of_the_key}")
    
    def remove_key(self, key_code, file_name):
        remove(file_name)
        self.keys_stored.pop(key_code, False)
        loggerINFO(f"removed stored key with code: {key_code}")



