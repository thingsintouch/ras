from pprint import PrettyPrinter
pPrint = PrettyPrinter(indent=1).pprint

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
from os.path import isfile, exists
import dbus
import sys
import fcntl

progname = "com.example.HelloWorld"
objpath  = "/HelloWorld"
intfname = "com.example.HelloWorldInterface"
methname = 'SayHello'



params = Params(db=co.PARAMS)
conf_contents = '<?xml version="1.0" encoding="UTF-8"?> \n \
<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN"\n \
"http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">\n \
<busconfig>\n \
  <type>system</type>\n \
  <!-- Only root can own the service -->\n \
  <policy user="root">\n \
    <allow own="com.example.HelloWorld"/>\n \
    <allow send_destination="com.example.HelloWorld"/>\n \
    <allow send_interface="com.example.HelloWorld"/>\n \
  </policy><!-- Allow anyone to invoke methods on the interfaces -->\n \
  <policy context="default">\n \
    <allow send_destination="com.example.HelloWorld"/>\n \
    <allow send_interface="com.example.HelloWorld"/>\n \
  </policy>\n \
</busconfig>\n '

wpa_conf_1 ='ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev \n \
update_config=1\n \
\n \
network={ \n \
        ssid="'

wpa_conf_2 = '"\n \
        psk="'

wpa_conf_3 = '"\n \
}\n \
'

def on_ethernet():
    if exists(co.ETHERNET_FLAG_FILE):
        with open(co.ETHERNET_FLAG_FILE, encoding="utf-8") as f:
            ethernet_status = f.read(1)
        if ethernet_status == "1":
            return True
    return False

def store_wifi(wifi_network, wifi_password):
    try:
        params.put("wifi_network", wifi_network)
        params.put("wifi_password", wifi_password)
        loggerDEBUG(f"store_wifi - {wifi_network} {wifi_password}")
    except Exception as e:
        loggerDEBUG(f"store_wifi - Exception: {e}")

def get_wifi():
    wifi_network = False
    wifi_password = False
    try:
        wifi_network = params.get("wifi_network")
        wifi_password = params.get("wifi_password")
        loggerDEBUG(f"get wifi - {wifi_network} {wifi_password}")
    except Exception as e:
        loggerDEBUG(f"get wifi - Exception: {e}")
    return wifi_network, wifi_password

def create_conf_file():
    try:
        with open('/etc/dbus-1/system.d/com.example.HelloWorld.conf', 'w') as f:
            f.write(conf_contents)
        loggerDEBUG("inside create_conf_file ---------------------+---+-+-+-+")
    except Exception as e:
        loggerDEBUG(f"create_conf_file - Exception: {e}")

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
        loggerERROR(f"error on shell command: {command}")
        return False

rs = runShellCommand_and_returnOutput

def is_enabled(service):
    result = False
    try:
        answer = rs("sudo systemctl is-enabled "+service)
        loggerDEBUG(f"answer is_enabled({service}): {answer}")
        if "enabled" in str(answer): result=True
    except Exception as e:
        loggerDEBUG(f"is_enabled({service})- Exception: {e}")
    loggerDEBUG(f"is_enabled({service})- result: {result}")
    return result

def are_the_right_service_configurations_in_place():
    if is_enabled("dhcpcd") and not is_enabled("NetworkManager"): 
        return True
    else:
        return False

def copy_the_predefined_interfaces_file():
    try:
        rs("sudo cp /home/pi/ras/common/interfaces /etc/network")
    except Exception as e:
        loggerDEBUG(f"copy_the_predefined_interfaces_file()- Exception: {e}")

def copy_wpa_supp_conf_to_boot():
    try:
        rs("sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /boot")
    except Exception as e:
        loggerDEBUG(f"copy_wpa_supp_conf_to_boot()- Exception: {e}")

def restart_dhcp_service():
    try:
        rs("sudo systemctl restart dhcpcd")
    except Exception as e:
        loggerDEBUG(f"restart_dhcp_service- Exception: {e}")

def reboot():
    os.system("sudo reboot")
    time.sleep(60)
    sys.exit(0) 

def enable_service(service):
    try:
        rs("sudo systemctl enable "+service)
    except Exception as e:
        loggerDEBUG(f"enable_service({service})- Exception: {e}")

def disable_service(service):
    try:
        rs("sudo systemctl disable "+service)
    except Exception as e:
        loggerDEBUG(f"enable_service({service})- Exception: {e}")

def start_service(service):
    try:
        rs("sudo systemctl start "+service)
    except Exception as e:
        loggerDEBUG(f"start_service({service})- Exception: {e}")

def stop_service(service):
    try:
        rs("sudo systemctl stop "+service)
    except Exception as e:
        loggerDEBUG(f"stop_service({service})- Exception: {e}")

def connect_to_wifi_through_d_bus_method():
    while on_ethernet():
        time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)
    try:
        bus = dbus.SystemBus()
        obj = bus.get_object(progname, objpath)
        interface = dbus.Interface(obj, intfname)     # Get the interface to obj
        method = interface.get_dbus_method(methname)
        method("some_string")
        loggerDEBUG("inside connect_to_wifi_through_d_bus_method ************************************")
    except Exception as e:
        loggerDEBUG(f"connect_to_wifi_through_d_bus_method - Exception: {e}")

def prepare_wpa_supplicant_conf_file():
    try:
        wifi_network, wifi_password = get_wifi()
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
            file_content = wpa_conf_1 + wifi_network + wpa_conf_2 + \
                wifi_password + wpa_conf_3
            f.write(file_content)
        #copy_wpa_supp_conf_to_boot()
        loggerDEBUG("inside prepare_wpa_supplicant_conf_file ---------------------+---+-+-+-+")
    except Exception as e:
        loggerDEBUG(f"prepare_wpa_supplicant_conf_file - Exception: {e}")

def connect_to_wifi_using_wpa_cli():
    while on_ethernet():
        time.sleep(co.PERIOD_CONNECTIVITY_MANAGER)
    try:
        prepare_wpa_supplicant_conf_file()
        params.put("rebootTerminal","1")
        loggerDEBUG("inside connect_to_wifi_using_wpa_cli ************************************")
    except Exception as e:
        loggerDEBUG(f"connect_to_wifi_using_wpa_cli - Exception: {e}")


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
    keys_to_store = keys_by_Type[TxType.FACTORY_SETTINGS] + \
                    keys_by_Type[TxType.FACTORY_DEFAULT_VALUES]
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

def manage_wifi_network_name_with_spaces(wifi_network):
    wifi_network_for_cli_command = False
    try:
        if " " in wifi_network:
            wifi_network_for_cli_command = "'" + wifi_network + "'"
        else:
            wifi_network_for_cli_command = wifi_network
    except Exception as e:
        loggerDEBUG(f"manage_wifi_network_name_with_spaces- Exception: {e}")
    return wifi_network_for_cli_command

def setup_wpa_supplicant():
    copy_the_predefined_interfaces_file()
    copy_wpa_supp_conf_to_boot()
    enable_service("dhcpcd")
    disable_service("NetworkManager")
    start_service("dhcpcd")
    time.sleep(5)
    stop_service("NetworkManager")
    time.sleep(5)
    reboot()

def ensure_wpa_supplicant():
    if on_ethernet():
        if not are_the_right_service_configurations_in_place():
            setup_wpa_supplicant()

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        fcntl.flock(file, fcntl.LOCK_EX)  # Acquire an exclusive lock
        file.write(content)
        fcntl.flock(file, fcntl.LOCK_UN)  # Release the lock