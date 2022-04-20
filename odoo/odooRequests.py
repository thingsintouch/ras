import requests
import json

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from common.common import get_own_IP_address, pPrint
from common.connectivity import extract_odoo_host_and_port

from common.constants import PARAMS, ROUTE_INCOMING_IN_ODOO, QUESTION_ASK_FOR_REGISTER_CLOCKINGS
from common.params import Params

params = Params(db=PARAMS)
productName = params.get('productName')
headers     = {'Content-Type': 'application/json'}

def post_request_and_get_answer(requestURL, payload):
    try:
        if params.get("odooPortOpen") == "1":
            
            posting     = requests.post(url=requestURL, json=payload, headers=headers, verify= False, timeout=150000)
            
            if params.get("odooPortOpen") != "0" and posting.status_code == 404:
                loggerINFO(f"Route is not recognized by Odoo anymore, RAS has to be registered again")
                loggerINFO(f"odooConnectedAtLeastOnce set to 0")
                params.put("odooConnectedAtLeastOnce", "0")
                params.put("RASxxx", "ras2.eu")
                answer = {"error": "404"}
            else:
                answer = posting.json().get("result", False)
        else:
            answer = {"error": "Odoo Port Closed"}

    except ConnectionRefusedError as e:
        loggerDEBUG(f"post_request_and_get_answer - ConnectionRefusedError - Request Exception : {e}")
        answer = {"error": "ConnectionRefusedError"}

    except Exception as e:
        loggerDEBUG(f"post_request_and_get_answer not Available - Exception: {e}")
        answer = {"error": str(e)}

    loggerDEBUG(f"in post_request_and_get_answer - requestURL {requestURL} -payload {payload} -answer: {answer}")
    return answer

def postToOdooRegisterClockings(clockings):
    """ 
        Returns answer from Odoo for Making aa ASYNC hronous Clocking
        with a list of clockings (format: "card"+"-"+"timestamp in sec")
    """
    requestURL  = params.get("odooUrlTemplate") +  ROUTE_INCOMING_IN_ODOO + \
              "/" + params.get("routefromDeviceToOdoo")
    payload     = {
                'question'      : str(QUESTION_ASK_FOR_REGISTER_CLOCKINGS),
                'productName'   : str(productName),
                'clockings'     : clockings
                }
    return post_request_and_get_answer(requestURL, payload)





