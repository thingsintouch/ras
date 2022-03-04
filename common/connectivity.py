import subprocess
import socket

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from common.params import Params
from common import constants as co


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

def internetReachable():
    internet_reachable = isPingable("1.1.1.1")
    params.put("internetReachable", internet_reachable)
    return internet_reachable

def clean_string_after_slash(to_clean):
    return to_clean.split("/", 1)[0]

def store_host_port_and_template(scheme,host,port):
    if scheme:
        template = scheme+"://"+host+":"+port
    else:
        template = host+":"+port
    params.put("odoo_host", host)
    params.put("odoo_port", port)
    params.put("odooUrlTemplate", template)
    loggerINFO(f"stored in db params - template: {template}, host: {host}, port: {port}")

def extract_odoo_host_and_port(odooAddress = False):
    if not odooAddress:
        odooAddress = params.get("odooUrlTemplate")
    loggerDEBUG(f"extract_odoo_host_and_port() - odooAddress {odooAddress}")
    if odooAddress is not None:
        odooAdressSplitted = odooAddress.split(":")
        length = len(odooAdressSplitted)
        loggerINFO(f"odooAdressSplitted {odooAdressSplitted} - length {length}")
        
        if length == 1:
            scheme  = ""
            host    = clean_string_after_slash(odooAdressSplitted[0])
            port    = "443"
        if length == 2:
            zero = odooAdressSplitted[0]
            one = odooAdressSplitted[1].replace('//','')
            if zero == "https":
                scheme  = "https"
                host    = clean_string_after_slash(one)
                port    = "443"
            elif zero == "http":
                scheme  = "http"
                host    = clean_string_after_slash(one)
                port    = "8069"
            else:
                scheme  = "https"
                host    = clean_string_after_slash(zero)
                port    = clean_string_after_slash(one)
        if length == 3:
            if "//" in odooAdressSplitted[1]:
                scheme  = odooAdressSplitted[0]
                host    = clean_string_after_slash(odooAdressSplitted[1].replace('//',''))
                port    = clean_string_after_slash(odooAdressSplitted[2])
            else:
                scheme  = ""
                host    = "0"
                port    = "0"
        store_host_port_and_template(scheme, host, port)


def isOdooPortOpen():
    try:
        odooHost = params.get("odoo_host")
        odooPort = params.get("odoo_port")
        #loggerDEBUG(f"odoo_host {odooHost}- odoo_port {odooPort}")
        if odooHost is None or odooPort is None:
            extract_odoo_host_and_port()
            odoo_port_open = False
        if odooPort.isnumeric():
            odooPort =  int(odooPort)
            odoo_port_open = isIpPortOpen((odooHost, odooPort))
        else:
            odoo_port_open = False
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
        loggerDEBUG(f"---------- ipPort: {ipPort}")
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
