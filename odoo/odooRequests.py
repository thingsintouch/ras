import requests
import json

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from common.common import get_own_IP_address

def register_async_clocking(template, serial, passphrase, card_code_and_timestamp):
    """ 
        Returns answer from Odoo for Making aa ASYNC hronous Clocking
        with rfid_card_code
        It will register the Timestamp based on the Clock of the Odoo Server.
        serial is the serial of the input (not the serial of the device)
    """

    try:
        requestURL  = template + "/iot/" + str(serial) + "/action"
        payload     = {'passphrase': str(passphrase), "value": str(card_code_and_timestamp)}
        loggerDEBUG(f"in register_clocking() - requestURL: {requestURL}, payload: {payload}")

        posting     = requests.post(url=requestURL, data=payload)
        answer      = posting.json()        
        loggerINFO(f"in register_clocking - answer: {answer}")     

        return answer

    except ConnectionRefusedError as e:
        loggerDEBUG(f"register_clocking not Available - ConnectionRefusedError - Request Exception : {e}")

    except Exception as e:
        loggerDEBUG(f"register_clocking not Available - Exception: {e}")
    
    return False 

def register_sync_clocking(template, serial, passphrase, rfid_card_code):
    """ 
        Returns answer from Odoo for Making a Synchronous Clocking
        with rfid_card_code
        It will register the Timestamp based on the Clock of the Odoo Server.
        serial is the serial of the input (not the serial of the device)
    """

    try:
        requestURL  = template + "/iot/" + str(serial) + "/action"
        payload     = {'passphrase': str(passphrase), "value": str(rfid_card_code)}
        loggerDEBUG(f"in register_clocking() - requestURL: {requestURL}, payload: {payload}")

        posting     = requests.post(url=requestURL, data=payload)
        answer      = posting.json()        
        loggerINFO(f"in register_clocking - answer: {answer}")     

        return answer

    except ConnectionRefusedError as e:
        loggerDEBUG(f"register_clocking not Available - ConnectionRefusedError - Request Exception : {e}")

    except Exception as e:
        loggerDEBUG(f"register_clocking not Available - Exception: {e}")
    
    return False    

def check_if_registered(template, serial, passphrase):
    """ 
        Returns True if registered in Odoo
        serial is the serial of the input (not the serial of the device)
    """

    try:
        requestURL  = template + "/iot/" + str(serial) + "/check"
        payload     = {'passphrase': str(passphrase)}
        loggerDEBUG(f"in check_if_registered() - requestURL: {requestURL}, payload: {payload}")

        posting     = requests.post(url=requestURL, data=payload)
        answer      = posting.json()        
        loggerINFO(f"in check_if_registered() - answer: {answer}")     

        state       = answer.get("state", False)
        return state

    except ConnectionRefusedError as e:
        loggerDEBUG(f"Remote Odoo Control not Available - ConnectionRefusedError - Request Exception : {e}")

    except Exception as e:
        loggerDEBUG(f"Remote Odoo Control not Available - Exception: {e}")
    
    return False

def register_new_device_in_Odoo(odooAddress):
    """ 
        Returns  x x if registered in Odoo
        
    """

    try:
        requestURL  = odooAddress
        ownIpAddress = get_own_IP_address()
        payload     = {'template': 'thingsintouch.ras', 'ip': ownIpAddress}
        loggerDEBUG(f"in register_new_device_in_Odoo() - requestURL: {requestURL}, payload: {payload}")

        posting     = requests.post(url=requestURL, data=payload)
        answer      = posting.json()        
        loggerINFO(f"in register_new_device_in_Odoo() - answer: {answer}")     

        #state       = answer.get("state", False)
        return answer

    except ConnectionRefusedError as e:
        loggerDEBUG(f"register_new_device_in_Odoo() - ConnectionRefusedError - Request Exception : {e}")

    except Exception as e:
        loggerDEBUG(f"register_new_device_in_Odoo() - Exception: {e}")
    
    return False
