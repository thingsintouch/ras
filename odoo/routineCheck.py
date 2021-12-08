from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from odoo.odooRequests import routine_check

from common.constants import PARAMS
from common.params import Params

params              = Params(db=PARAMS)

def routineCheck():
    template             = params.get("odooUrlTemplate")
    serial               = params.get("serial_async")
    passphrase           = params.get("passphrase_async")
    to_send = {
        "param 1": "value 1",
        "param 2": "value 2",
        }
    try:
        answer = routine_check(template, serial, passphrase, to_send)
    except Exception as e:
        loggerDEBUG(f"Could not do ROUTINE CHECK - Exception: {e}")
        answer = False
    