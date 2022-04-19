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
from . import constants as co


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
        loggerINFO(f"Setting timezone: {timezone}")
        os.environ["TZ"] = timezone
        command3 = "TZ="+timezone+";export TZ "
        answer3 = runShellCommand_and_returnOutput(command3)
        time.tzset()
        command1 = "sudo rm -rf /etc/localtime"
        command2 = "sudo ln -s /usr/share/zoneinfo/"+timezone+" /etc/localtime"
        answer1 = runShellCommand_and_returnOutput(command1)
        answer2 = runShellCommand_and_returnOutput(command2)        
        loggerDEBUG(f"Timezone was set- answer1: {answer1}; answer2: {answer2}; answer3: {answer3}")
        return True
    except Exception as e:
        loggerERROR(f"exception in method setTimeZone (using tz database): {e}")
        return False

def set_device_time(timestamp):
    try:
        command = "sudo date -s '" + timestamp + "'"
        answer = runShellCommand_and_returnOutput(command)
        loggerDEBUG(f"set device time: {timestamp} with shell command answer {answer}")
        return True
    except Exception as e:
        loggerERROR(f"exception in method set_device_time: {e}")
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
    loggerDEBUG(f"machine id (= cpuinfo serial number) is {machine_id}")
    return machine_id 

def getHashedMachineId():
    machine_id = getMachineID()
    m = bytes(machine_id, 'utf-8')
    ds = co.HASH_DIGEST_SIZE
    k = co.HASH_KEY
    s = co.HASH_SALT

    hashed_machine_id = blake2b( m, \
        digest_size=ds,
        key=k,
        salt=s
        ).hexdigest()

    loggerDEBUG(f"hashed machine id: {hashed_machine_id}")

    return hashed_machine_id

def store_hashed_machine_id():
    if params.get('hashed_machine_id') is None:
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
    IP = '127.0.0.1'
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        loggerDEBUG(f"exception while getting the IP Address: {e}")
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
