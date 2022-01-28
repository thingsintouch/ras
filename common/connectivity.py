import subprocess
import socket

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from common.params import Params
from common import constants as co
from common.common import get_own_IP_address


params = Params(db=co.PARAMS)

def isSuccesRunningSubprocess(command):
    try:
        completed = subprocess.run(command.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        if completed.returncode == 0:
            return True
        else:
            return False
    except:
        return False  

def isPingable(address):
    command = "ping -c 1 " + address
    return isSuccesRunningSubprocess(command)

def internetReachable(): # in the local branch , we "fake" that internet is allways reachable
    internet_reachable = True
    params.put("internetReachable", internet_reachable)
    try:
        params.put("ownIpAddress", get_own_IP_address())
    except Exception as e:
        loggerDEBUG(f"exception while getting the IP Address: {e}")
    return internet_reachable

def extract_odoo_host_and_port():
    odooAddress = params.get("odooUrlTemplate")
    if odooAddress is not None:
        odooAdressSplitted = odooAddress.split(":")
        length = len(odooAdressSplitted)
        loggerINFO(f"odooAdressSplitted {odooAdressSplitted} - length {length}")
        if length == 1:
            params.put("odoo_host", odooAdressSplitted[0])
            params.put("odoo_port", "443")
        if length == 2:
            zero = odooAdressSplitted[0]
            one = odooAdressSplitted[1]
            if zero == "https":
                params.put("odoo_host", one)
                params.put("odoo_port","443")
            else:
                params.put("odoo_host", zero)
                params.put("odoo_port", one)
        if length == 3:
            if "//" in odooAdressSplitted[1]:
                odoo_host = odooAdressSplitted[1].replace('/','')
                params.put("odoo_host", odoo_host)
                params.put("odoo_port", odooAdressSplitted[2])
            else:
                params.put("odoo_host", "0")
                params.put("odoo_port", "0")
        odooHost = params.get("odoo_host")
        odooPort = params.get("odoo_port")
        loggerINFO(f"odoo_host {odooHost}- odoo_port {odooPort}")

def isOdooPortOpen():
    try:
       #odooHost = params.get("odoo_host")
       #odooPort = params.get("odoo_port")
        #loggerDEBUG(f"odoo_host {odooHost}- odoo_port {odooPort}")
        odooHost = "erp.priinc.com"
        odooPort = "443"
        if odooHost is None or odooPort is None:
            extract_odoo_host_and_port()
            return False
        if odooPort.isnumeric():
            odooPort =  int(odooPort)
            odoo_port_open = isIpPortOpen((odooHost, odooPort))
        else:
            return False
    except Exception as e:
        #extract_odoo_host_and_port()
        loggerDEBUG(f"common.connectivity - exception in method isOdooPortOpen: {e}")
        odoo_port_open = False
    params.put("odooPortOpen", odoo_port_open)
    return odoo_port_open

def isIpPortOpen(ipPort): # you can not ping ports, you have to use connect_ex for ports
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        canConnectResult = s.connect_ex(ipPort)
        if canConnectResult == 0:
            #print("Utils - IP Port OPEN ", ipPort)
            isOpen = True
        else:
            #print("Utils - IP Port CLOSED ", ipPort)
            isOpen = False
    except Exception as e:
        loggerERROR(f"common.connectivity - exception in method isIpPortOpen: {e}")
        isOpen = False
    finally:
        s.close()
    return isOpen
