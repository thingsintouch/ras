import os

from common import constants as co
from common.params import mkdirs_exists_ok

from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR

def make_sure_dir_KEYS_exists():
    if not os.path.exists(co.KEYS):
        mkdirs_exists_ok(co.KEYS)

def calculate_file_name(key):
        expiration_date = key.get("expiration_date", False)
        if not expiration_date:
            expiration_date = "0"
        return co.KEYS + "/" + str(key["unique_virtual_key"]) + "%" + str(expiration_date)

def store_iot_keys(keys):
    for key in keys:
        file_name_of_the_key = calculate_file_name(key)
        loggerINFO(f"file_name_of_the_key: {file_name_of_the_key}")
    return