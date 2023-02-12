import requests
import json

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from common.common import get_own_IP_address, pPrint, get_hashed_machine_id
from common.connectivity import extract_odoo_host_and_port

from common.constants import PARAMS
from common.params import Params

params = Params(db=PARAMS)

def get_iot_template():
    template = params.get("odooUrlTemplate") or ""
    return template + "/iot/"

def post_request_and_get_answer(requestURL, payload):

    try:
        if params.get("odooPortOpen") == "1":

            posting = requests.post(url=requestURL, data=payload, verify= False, timeout=150000)
            
            if params.get("odooPortOpen") != "0" and posting.status_code == 404:
                loggerINFO(f"Route is not recognized by Odoo anymore, RAS has to be registered again")
                loggerINFO(f"odooConnectedAtLeastOnce set to 0")
                params.put("odooConnectedAtLeastOnce", "0")
                params.put("isRemoteOdooControlAvailable", "0")
                # params.put("RASxxx", "ras2.eu")
                answer = {"error": "404"}
            else:
                answer = posting.json()
        else:
            answer = {"error": "Odoo Port Closed"}

    except ConnectionRefusedError as e:
        #loggerDEBUG(f"post_request_and_get_answer - ConnectionRefusedError - Request Exception : {e}")
        answer = {"error": "ConnectionRefusedError"}

    except Exception as e:
        #loggerDEBUG(f"post_request_and_get_answer not Available - Exception: {e}")
        answer = {"error": e}

    loggerDEBUG(f"in post_request_and_get_answer - requestURL {requestURL} -payload {payload} -answer: {answer}")
    return answer


def register_async_clocking(card_code, timestamp):
    """ 
        Returns answer from Odoo for Making aa ASYNC hronous Clocking
        with rfid_card_code
        It will register the Timestamp based on the Clock of the Odoo Server.
        serial is the serial of the input (not the serial of the device)
    """
    requestURL  = get_iot_template() + str(params.get("serial_async")) + "/action"
    payload     = {
        'passphrase'    : str(params.get("passphrase_async")),
        "card_code"     : str(card_code),
        "timestamp"     : int(timestamp)
        }
    return post_request_and_get_answer(requestURL, payload)

def call_lock_async(card_code, timestamp, state):
    """ 
        Returns answer from Odoo for Making aa ASYNC hronous CALL to open a lock
        with an rfid_card_code acting as a key.
        It will register the Timestamp based on the Clock of the Odoo Server.
        serial is the serial of the input (not the serial of the device)
    """
    requestURL  = get_iot_template() + str(params.get("serial_call_lock_async")) + "/action"
    payload     = {
        'passphrase'    : str(params.get("passphrase_call_lock_async")),
        "value"         : str(card_code),
        "timestamp"     : int(timestamp),
        "state"         : str(state)
        }
    return post_request_and_get_answer(requestURL, payload)

def call_lock_sync(card_code):
    """ 
        Returns answer from Odoo for Making a synchronous CALL to open a lock
        with an rfid_card_code acting as a key.
        It will register the Timestamp based on the Clock of the Odoo Server.
        serial is the serial of the input (not the serial of the device)
    """
    requestURL  = get_iot_template() + str(params.get("serial_call_lock_sync")) + "/action"
    payload     = {
        'passphrase'    : str(params.get("passphrase_call_lock_sync")),
        "value"     : str(card_code)
        }
    return post_request_and_get_answer(requestURL, payload)

def register_sync_clocking(rfid_card_code):
    """ 
        Returns answer from Odoo for Making a Synchronous Clocking
        with rfid_card_code
        It will register the Timestamp based on the Clock of the Odoo Server.
        serial is the serial of the input (not the serial of the device)
    """
    requestURL  = get_iot_template() + str(params.get("serial_sync")) + "/action"
    payload     = {
        'passphrase'    : str(params.get("passphrase_sync")),
        "value"         : str(rfid_card_code)
        }
    return post_request_and_get_answer(requestURL, payload)


def check_if_registered():
    """ 
        Returns True if registered in Odoo
        serial is the serial of the input (not the serial of the device)
    """
    requestURL  = get_iot_template() + str(params.get("serial_async")) + "/check"
    payload     = {
        'passphrase': str(params.get("passphrase_async"))
        }
    answer = post_request_and_get_answer(requestURL, payload)

    return answer.get("state", False)

def get_name_of_iot_template_to_register_new_device():
    template_name = params.get_filtered("template_to_register_device")
    if template_name == "not defined":
        template_name = 'thingsintouch.ras'
    return template_name

def register_new_device_in_Odoo(requestURL, payload):
    """ 
    x
    """
    
    extract_odoo_host_and_port(requestURL)

    payload['template'] = get_name_of_iot_template_to_register_new_device() #'thingsintouch.ras'
    payload['ip']       = get_own_IP_address()
    payload['hashed_machine_id'] = get_hashed_machine_id()
    print(f"template is {payload['template']}")
    print("payload of request to register a new device")
    pPrint(payload)

    try:
        posting = requests.post(url=requestURL, data=payload, verify=False)
        answer = posting.json()
        print("answer to a request to register a new device")
        pPrint(answer)
    except Exception as e:
        loggerDEBUG(f"REGISTER NEW DEVICE - answer not Available - Exception: {e}")
        answer = False

    return answer


def routine_check(payload):
    """ 
        Returns answer from Odoo 
    """
    requestURL  = get_iot_template() + str(params.get("serial_routine")) + "/action"
    payload.update({
        'passphrase': str(params.get("passphrase_routine")),
        })
    return post_request_and_get_answer(requestURL, payload)

def request_get_iot_keys(payload):
    """ 
        Returns answer from Odoo 
    """
    requestURL  = get_iot_template() + str(params.get("serial_get_iot_keys")) + "/action"
    payload.update({
        'passphrase': str(params.get("passphrase_get_iot_keys")),
        })
    return post_request_and_get_answer(requestURL, payload)

