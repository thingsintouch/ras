import requests
import json
import os

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
import common.constants as co
import common.common as cc
#import lib.Utils as ut
import common.logger as lo
from common.constants import PARAMS
from common.params import Params, Log
from common.keys import TxType


params = Params(db=PARAMS)
log_db =  Log()

def getPayload(settings_to_send):
    payload = {}
    inc_log = log_db.get_whole_log()
    params.put('incrementalLog', inc_log)
    for s in settings_to_send:
        try:
            payload[s] = params.get(s)
        except Exception as e:
            loggerERROR(f"Exception while trying to access setting {s}")
    #cc.pPrint(payload)
    return payload

def acknowledgeTerminalInOdoo():
    terminal_ID_in_Odoo = False

    template = params.get("odooUrlTemplate")
    if template is None: return False

    params.put("ownIpAddress", cc.get_own_IP_address())
    try:
        loggerDEBUG(f"params.get(odooUrlTemplate) {template} . co.ROUTE_ACK_GATE {co.ROUTE_ACK_GATE} ")
        requestURL  = template + co.ROUTE_ACK_GATE
        
        headers     = {'Content-Type': 'application/json'}
        list_of_all_keys = params.get_list_of_all_keys()
        list_on_ack_from_odoo = params.get_list_of_keys_with_type(TxType.ON_ACK_FROM_ODOO)
        #print("ww"*80)
        #cc.pPrint(list_on_ack_from_odoo)
        payload     = getPayload(list_of_all_keys)

        response    = requests.post(url=requestURL, json=payload, headers=headers, verify=False)

        loggerDEBUG(f"Acknowledge Terminal in Odoo - Status code of response: {response.status_code} ")
        if params.get("odooPortOpen") != "0" and response.status_code == 404:
            loggerINFO(f"Route is not recognized by Odoo anymore, RAS has to be registered again")
            loggerINFO(f"odooConnectedAtLeastOnce set to 0")
            params.put("odooConnectedAtLeastOnce", "0")
            params.put("RASxxx", "RASxxx")
        else:
            #loggerDEBUG("Printing Entire Post Response")
            #cc.pPrint(response.json())
            #loggerDEBUG("Printing list_on_ack_from_odoo")
            #cc.pPrint(list_on_ack_from_odoo)
            answer = response.json().get("result", None)
            if answer:
                error = answer.get("error", None)
                if error:
                    loggerINFO(f"could not acknowledge the terminal in Odoo- error: {error}")
                else:
                    for o in list_on_ack_from_odoo:
                        value = answer.get(o, False)
                        loggerDEBUG(f"key: {o}; value:{value} ") 
                        if type(value) != bool : value = str(value)
                        params.put(o,value)
                    if answer["tz"]:
                        loggerDEBUG(f"setting time zone to {answer['tz']}")
                        cc.setTimeZone()
                    params.put("acknowledged", True)
            else:
                loggerINFO(f"Answer from Odoo did not contain an answer")
    except ConnectionRefusedError as e:
        loggerINFO(f"Request Exception : {e}")
        # TODO inform the user via Display and wait 1 second
    except Exception as e:
        loggerDEBUG(f"Could not acknowledge Terminal in Odoo - Exception: {e}")
        # TODO inform the user via Display and wait 1 second

    return terminal_ID_in_Odoo


def resetSettings():
    try:
        requestURL  = params.get("odooUrlTemplate") + \
            co.ROUTE_INCOMING_IN_ODOO + "/" + params.get("routefromDeviceToOdoo")
        headers     = {'Content-Type': 'application/json'}
        productName = params.get('productName')
        payload     = {'question': co.QUESTION_ASK_FOR_RESET_SETTINGS,
                    'productName': productName}

        response    = requests.post(url=requestURL, json=payload, headers=headers, verify=False)

        # print("resetSettings Status code: ", response.status_code)
        # print("resetSettings Printing Entire Post Response")
        # print(response.json())
        answer = response.json().get("result", None)
        if answer:
            error = answer.get("error", None)
            params.put("isRemoteOdooControlAvailable", "1")
            if error:
                loggerINFO(f"resetSettings not Available - error in answer from Odoo: {error}")
                return False
            else:
                loggerINFO(f"resetSettings was successful - {answer}")
                return True
        else:
            loggerINFO(f"resetSettings not Available - Answer from Odoo did not contain an answer")        
    except ConnectionRefusedError as e:
        loggerERROR(f"resetSettings not Available - ConnectionRefusedError - Request Exception : {e}")
    except Exception as e:
        loggerERROR(f"resetSettings not Available - Exception: {e}")

    params.put("isRemoteOdooControlAvailable", "0")
    return False     
