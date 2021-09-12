from pprint import PrettyPrinter
pPrint = PrettyPrinter(indent=1).pprint

#import time
import subprocess
import os
import time
import socket

from hashlib import blake2b

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from . import constants as co
import lib.Utils as ut
from dicts import tz_dic
from common.params import Params
import common.constants as co
from common.keys import keys_by_Type, TxType
from factory_settings.custom_params import factory_settings


params = Params(db=co.PARAMS)

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

def setTimeZone():
    try: 
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
    try:
        with open(co.MACHINE_ID_FILE,"r")as f:
            machine_id= bytes(f.readline().replace('\n',''), encoding='utf8')
        #loggerDEBUG(f"got machine ID: {machine_id}")
    except Exception as e:
        loggerERROR(f"Exception while retreiving Machine ID from its file: {e}")
        machine_id = None
    if not machine_id:
        #TODO generate machine_id randomly and write it to machineID
        loggerINFO(f"No MACHINE ID found.") # A random MACHINE ID will be generated and saved. 
        pass
    return machine_id 

def getHashedMachineId():
    machine_id = getMachineID()

    hashed_machine_id = blake2b( \
        machine_id,
        digest_size=co.HASH_DIGEST_SIZE,
        key=co.HASH_KEY,
        salt=co.HASH_SALT,
        person=co.HASH_PERSON_REGISTER_TERMINAL, 
        ).hexdigest()

    return hashed_machine_id

def store_hashed_machine_id():
    hashed_machine_id = getHashedMachineId()
    params.put('hashed_machine_id', hashed_machine_id)

def store_factory_settings_in_database():
    if params.get("odooConnectedAtLeastOnce") != "1":
        for k in keys_by_Type[TxType.FACTORY_SETTINGS]:
            try:
                loggerDEBUG(f"key: {k} - params get k {params.get(k)}")
                if params.get(k) is None:
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
