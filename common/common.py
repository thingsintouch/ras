from pprint import PrettyPrinter
pPrint = PrettyPrinter(indent=1).pprint

#import time
import subprocess
import os
import time
import socket
import secrets

from hashlib import blake2b

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from common.params import Params
import common.constants as co
from common.keys import keys_by_Type, TxType
from factory_settings.custom_params import factory_settings
from os.path import isfile


params = Params(db=co.PARAMS)



def store_wifi_network_and_password(wifi_network, wifi_password):
    params.put("wifi_network", wifi_network)
    params.put("wifi_password", wifi_password)
    return True

def get_wifi_network_and_password():
    wifi_network=False
    wifi_password=False
    try:
        wifi_network =params.get("wifi_network")
        wifi_password =params.get("wifi_password")
    except Exception as e:
        loggerDEBUG(f"get_wifi_network_and_password - Exception: {e}")
    return wifi_network, wifi_password 

def prettyPrint(message):
    pPrint(message)

def runShellCommand(command):
    try:
        completed = subprocess.run(command.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        loggerDEBUG(f'shell command {command} - returncode: {completed.returncode}')
        return completed.returncode
    except:
        loggerERROR(f"error on shell command: {command}")
        return False

def runShellCommand_and_returnOutput(command):
    try:
        completed = subprocess.check_output(command, shell=True)
        #loggerDEBUG(f'shell command {command} - returncode: {completed}')
        return str(completed, 'utf-8', 'ignore')
    except:
        #loggerERROR(f"error on shell command: {command}")
        return False

def setTimeZone(tz = False):
    try:
        if tz:
            timezone = tz
        else:
            timezone = params.get("tz")
        #print(timezone)
        os.environ["TZ"] = timezone
        time.tzset()
        loggerINFO(f"Timezone: {timezone} - was set using tz database")
        return True
    except Exception as e:
        loggerERROR(f"exception in method setTimeZone (using tz database): {e}")
        return False

def getMachineID():
    # Extract serial from cpuinfo file
    try:
        with open('/proc/cpuinfo','r') as f:
            for line in f:
                if 'Serial' in line:
                    machine_id = line[10:26]
    except Exception as e:
        loggerERROR(f"Exception while getting serial number from cpuinfo file : {e}, machine_id gets random id")
        machine_id = secrets.token_hex(16)
    loggerDEBUG(f"machine id (= cpuinfo serial number (or random when there was an Exception)) is {machine_id}")
    return machine_id 

def computeHashedMachineId():
    machine_id = bytes(getMachineID(), encoding='utf8')

    hashed_machine_id = blake2b( \
        machine_id,
        digest_size=co.HASH_DIGEST_SIZE,
        key=co.HASH_KEY,
        salt=co.HASH_SALT,
        person=co.HASH_PERSON_REGISTER_TERMINAL, 
        ).hexdigest()

    return hashed_machine_id

def get_hashed_machine_id():
    hashed_machine_id = params.get('hashed_machine_id')
    if hashed_machine_id is None:
        hashed_machine_id = computeHashedMachineId()
        params.put('hashed_machine_id', hashed_machine_id)
    return hashed_machine_id

def store_factory_settings_in_database():    
    #if params.get("odooConnectedAtLeastOnce") != "1":
    keys_to_store = keys_by_Type[TxType.FACTORY_SETTINGS] + \
                    keys_by_Type[TxType.FACTORY_DEFAULT_VALUES]
    # loggerDEBUG(f"keys to store {keys_to_store}")
    # prettyPrint(keys_to_store)
    for k in keys_to_store:
        try:
            if params.get(k) is None:
                loggerDEBUG("-"*80)
                loggerDEBUG(f"key: {k} - stored value in params db: {params.get(k)}")
                loggerDEBUG(f"key: {k} - storing value of factory_settings: {factory_settings[k]}")
                params.put(k, factory_settings[k])
        except Exception as e:
            loggerDEBUG(f"exception while storing factory setting {k}: {e}")

def set_bluetooth_device_name():
    # RASxxx = params.get('RASxxx')
    # if RASxxx is None or RASxxx == "not defined":
    #     bluetooth_device_name = "RAS - thingsintouch.com"
    # else:
    #     bluetooth_device_name = RASxxx
    bluetooth_device_name = "RAS - thingsintouch.com" # have to change ionic app
    params.put("bluetooth_device_name", bluetooth_device_name)

def get_own_IP_address():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    params.put("ip", IP)
    return IP

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
        loggerERROR(f"Utils - exception in method isIpPortOpen: {e}")
        isOpen = False
    finally:
        s.close()
    return isOpen

def ensure_git_does_not_change_env_file():
    try:
        #runShellCommand("cd /home/pi/ras")
        runShellCommand("sudo git update-index --skip-worktree .env")
    except Exception as e:
        loggerDEBUG(f"ensure_git_does_not_change_env_file -- Exception: {e}")

def get_period(period_name):
    try:
        n = params.get(period_name)
        default = co.DEFAULT_MINIMUM_PERIOD
        if n is None:
            period = default
        elif n:
            period = int(n)
            if period < default:
                period = default
        else:
            period = default
    except Exception as e:
        loggerDEBUG(f"exception in  get_period for {period_name}: {e} - period set to 14s")
        period = 14     
    return period

def BLOCKING_waiting_until_RAS_acknowledged_from_Odoo():
    while params.get("acknowledged") != "1":
        time.sleep(16) # waiting_to_be_acknowledged

def ensure_python_dependencies():
    def check_dependencies_for_3_7():
        #if params.get("dependencies_v3_7") != "1":
        files_for_dependencies = [
            ('/usr/local/lib/python3.7/dist-packages/werkzeug/__init__.py', "2.0.3"),
            ('/usr/local/lib/python3.7/dist-packages/flask_wtf/__init__.py', "1.0.1"),
            ('/usr/local/lib/python3.7/dist-packages/flask_login/__about__.py', '("0", "6", "1")'),
            ('/usr/local/lib/python3.7/dist-packages/pytz/__init__.py','2022.2.1')
            ]
        for f in files_for_dependencies:
            if not isfile(f[0]):
                return False
        for f in files_for_dependencies:
            with open(f[0]) as myfile:
                if not f[1] in myfile.read():
                    return False
        params.put("dependencies_v3_7", "1")
        return True

    if not check_dependencies_for_3_7():
        loggerINFO("-----############### install python dependencies for v3.7 ##########------")
        os.system("sudo sh /home/pi/ras/common/dependencies_for_3_7.sh")
        time.sleep(40)
        sys.exit(0) 
    else:
        loggerINFO("-----############### python dependencies for v3.7 already installed ##########------")

def delete_RAS_WiFi_connection():
    try:
        runShellCommand_and_returnOutput('sudo nmcli c delete "RAS"')
    except Exception as e:
        loggerDEBUG(f"delete_RAS_____WiFi_connection- Exception: {e}")

def manage_wifi_network_name_with_spaces(wifi_network):
    if " " in wifi_network:
        wifi_network_for_cli_command = "'" + wifi_network + "'"
    else:
        wifi_network_for_cli_command = wifi_network
    return wifi_network_for_cli_command

def connect_to_new_wifi_network():
    wifi_network, wifi_password = get_wifi_network_and_password()
    delete_RAS_WiFi_connection()
    wifi_network_for_cli_command = manage_wifi_network_name_with_spaces(wifi_network)
    answer = (runShellCommand_and_returnOutput('sudo nmcli dev wifi con '+wifi_network_for_cli_command+' password '+wifi_password+' name "RAS"'))
    connection_successful= False
    try:
        if "successfully activated" in answer:
            connection_successful= True
    except Exception as e:
        loggerDEBUG(f"Exception while connecting to WiFi network: {e}")
    return connection_successful