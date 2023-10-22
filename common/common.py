from pprint import PrettyPrinter
pPrint = PrettyPrinter(indent=1).pprint

import subprocess
import os
import time
import socket
import secrets
import random
import re

from hashlib import blake2b

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL

from common.params import Params
import common.constants as co
from common.keys import keys_by_Type, TxType
from factory_settings.custom_params import factory_settings
from os.path import isfile, exists, join
import dbus
import sys
import fcntl

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import pytz

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
    # employs UDP broadcast to retrieve the local IP address. The choice of '10.255.255.255' 
    # as the IP address is commonly used for this purpose, as it's a broadcast address 
    # that reaches all devices within the local network
    # It's plausible that certain networks or firewalls might impose restrictions 
    # or block UDP broadcast packets.
    # So, the device could be connected but show on the display "not connected".
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        st.settimeout(2)  # Set a timeout for socket operations
        IP = st.getsockname()[0]
    except Exception as e:
        loggerDEBUG(f"Exception while retrieving IP address making a UDP broadcast: {e}")
        IP = '127.0.0.1'
    finally:
        st.close()
    # if IP == '127.0.0.1':
    #     IP = get_own_IP_address_with_google()
    params.put("ip", IP)
    return IP

def get_own_IP_address_with_google():
    try:
        # Create a temporary socket to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)  # Set a timeout for socket operations

        # Connect to a remote server (Google's DNS server)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address from the socket's address
        local_ip = s.getsockname()[0]

    except socket.error as e:
        loggerDEBUG(f"Error while retrieving IP address contacting 8.8.8.8 (google): {e}")
        local_ip = '127.0.0.1'
    
    except Exception as e:
        loggerDEBUG(f"Exception while retrieving IP address contacting 8.8.8.8 (google): {e}")
        local_ip = '127.0.0.1'

    finally:
        s.close()

    return local_ip

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
    try:
        with open(filename, 'w') as file:
            fcntl.flock(file, fcntl.LOCK_EX)  # Acquire an exclusive lock
            file.write(str(content))
            fcntl.flock(file, fcntl.LOCK_UN)
    except Exception as e:
            loggerERROR(f"could not release the lock on {filename} while writing {content} in it - Exception {e}")

def initialize_show_debug_messages():
    if params.get("show_debug") is None:
        params.put("show_debug", "0")

def get_MAC_address(network_interface): # wlan0 or eth0
    MAC_address = None
    try:
        with open('/sys/class/net/'+network_interface+'/address', 'r') as file:
            MAC_address = file.read().strip()
    except FileNotFoundError:
        loggerDEBUG(f"Error: File '/sys/class/net/{network_interface}/address' not found.")
    except Exception as e:
        loggerDEBUG(f"get_MAC_address {network_interface} - Exception: {e}")
    loggerDEBUG(f"get_MAC_address- returns: {network_interface} {MAC_address}")
    return MAC_address

def generate_random_eth0_MAC_address(oui):
    # Generate the remaining 3 bytes (xx:xx:xx) of the MAC address
    random_bytes = [random.randint(0x00, 0xFF) for _ in range(3)]

    # Format the random bytes into hexadecimal strings
    random_bytes_str = [format(byte, '02x') for byte in random_bytes]

    eth0_address = ":".join([oui] + random_bytes_str)
    return eth0_address

def generate_eth0_MAC_address(oui, wlan0_MAC_address):
    if wlan0_MAC_address is None:
        return None

    # Validate that the wlan0_MAC_address is in the correct format "xx:xx:xx:xx:xx:xx"
    mac_parts = wlan0_MAC_address.split(":")
    if len(mac_parts) != 6:
        return None

    # Substitute the first three parts of the MAC address with oui
    eth0_MAC_address = ":".join([oui] + mac_parts[3:])
    return eth0_MAC_address

def set_eth0_MAC_address(new_MAC_address):
    try:
        rs("sudo ifconfig eth0 down")
        rs("sudo ifconfig eth0 hw ether "+new_MAC_address)
        rs("sudo ifconfig eth0 up")
        params.put("eth0_MAC_address", new_MAC_address)
    except Exception as e:
        loggerDEBUG(f"set_eth0_MAC_address {new_MAC_address} - Exception: {e}")

def set_oui(wlan0_MAC_address):
    # The OUI (Organizationally Unique Identifier)
    # 28:CD:C1 Raspberry Pi Trading Ltd
    # 3A:35:41 Raspberry Pi (Trading) Ltd
    # B8:27:EB Raspberry Pi Foundation
    # D8:3A:DD Raspberry Pi Trading Ltd
    # DC:A6:32 Raspberry Pi Trading Ltd
    # E4:5F:01 Raspberry Pi Trading Ltd
    if wlan0_MAC_address is not None and "b8:27:eb" in wlan0_MAC_address[:9]:
        oui = "28:cd:c1"
    else:
        oui = "b8:27:ec"
    return oui

def get_self_generated_eth0_MAC_address():
    wlan0_MAC_address = get_MAC_address("wlan0")
    params.put("wlan0_MAC_address", wlan0_MAC_address)
    oui = set_oui(wlan0_MAC_address)
    eth0_MAC_address = generate_eth0_MAC_address(oui, wlan0_MAC_address)
    if eth0_MAC_address is None:
        generate_random_eth0_MAC_address(oui)
    loggerDEBUG(f"eth0_MAC_address {eth0_MAC_address}")
    loggerDEBUG(f"wlan0_MAC_address {wlan0_MAC_address}")
    return eth0_MAC_address

def store_permanently_eth0_ḾAC_address(eth0_MAC_address):
    try:
        file_name = "/etc/systemd/network/99-default.link"
        rs("sudo rm " + file_name)
        lines_to_write = [
            "[Match]",
            "OriginalName=eth0",
            " ",
            "[Link]",
            "MACAddress="+eth0_MAC_address
        ]
        # Open the file in write mode (or create if it doesn't exist)
        with open(file_name, "w") as file:
            for line in lines_to_write:
                file.write(line + "\n")
        loggerINFO(f"successfully stored permanently_eth0_ḾAC_address {eth0_MAC_address}")    
    except Exception as e:
        loggerINFO(f"store_permanently_eth0_ḾAC_address {eth0_MAC_address} - Exception: {e}")    


def use_self_generated_eth0_MAC_address():
    eth0_MAC_address = get_self_generated_eth0_MAC_address()
    set_eth0_MAC_address(eth0_MAC_address)
    store_permanently_eth0_ḾAC_address(eth0_MAC_address)

def check_if_eth_mac_is_set():
    if params.get("use_self_generated_eth0_MAC_address")=="1":
        stored_mac_address = params.get("eth0_MAC_address")
        if stored_mac_address is None:
            stored_mac_address = get_self_generated_eth0_MAC_address()
        loggerDEBUG(f"ethernet mac stored {stored_mac_address} - used {get_MAC_address('eth0')}")
        if get_MAC_address("eth0") != stored_mac_address:
            params.put("setEthernetMAC", "1")
 
def initialize_eth0_MAC_address():
    if params.get("use_self_generated_eth0_MAC_address")==1:  #and params.get("eth0_MAC_address") is None
        use_self_generated_eth0_MAC_address()
    check_if_eth_mac_is_set()


def return_lines_from_file(file_path):
    try:
        # Read the existing file content
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        loggerDEBUG(f"File not found: {file_path}")
        lines = []
    return lines

# Email configuration
EMAIL_PROVIDER_SMTP_ADDRESS = 'smtp.gmail.com'
MY_EMAIL = 'logsras@gmail.com'

def send_email(email, subject, message_text, attachment_filename):
    try:
        # Create the email message
        message = MIMEMultipart()
        message['From'] = MY_EMAIL
        message['To'] = email
        message['Subject'] = subject

        # Attach the file if provided
        if attachment_filename:
            with open(attachment_filename, 'r') as file:
                lines = file.readlines()
            for line in lines:
                message_text = message_text + line

        # Attach the plain text message
        message.attach(MIMEText(message_text, 'plain'))

        with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS, timeout=20) as connection:
            connection.starttls()
            MY_PASSWORD = params.get("smtp_password") or False
            if MY_PASSWORD:
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:{subject}\n\n{message_text}".encode('utf-8')
                )
    except Exception as e:
        loggerDEBUG(f"Exception sending E-Mail: {e}")

def delete_file(file_path):
    with open(file_path, 'w') as lockfile:
        timeout = 1.1  # Specify your desired timeout in seconds
        start_time = time.time()
        locked = False
        while time.time() - start_time < timeout:
            try:
                fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                locked = True
                break
            except BlockingIOError:
                # Another process holds the lock; wait for a moment and retry
                time.sleep(0.05)
        if not locked:
            loggerINFO(f"Failed to acquire the lock for {file_path} that was set for deletion")
        else:
            try:
                os.remove(file_path)
            except Exception as e:
                loggerERROR(f"Failed to delete the file {file_path} - Exception: {e}")
        # Check if the file has been successfully deleted
    file_deleted = not exists(file_path)
    return file_deleted

def create_file(directory, file_name):
    if not exists(directory): os.makedirs(directory)
    file_path = join(directory, file_name)
    if not exists(file_path):
        with open(file_path, 'w') as f:
            pass

def get_timestamp_human(timestamp_int):
    try:
        tz = params.get("tz") or "Europe/Berlin"
        tzinfo = pytz.timezone(tz)
        timestamp_human = datetime.fromtimestamp(int(timestamp_int), tz=tzinfo).strftime('%H:%M:%S %A %d-%b-%y')
    except Exception as e:
        loggerINFO(f"could not calculate human readable timestamp from {timestamp_int} - Exception: {e}")
        timestamp_human = "unconverted timestamp " + str(timestamp_int)
    return timestamp_human

def mac_address_is_plausible(mac_address):
    if mac_address:
        # Regular expression pattern to match a valid MAC address
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        # Check if the string matches the MAC address pattern
        if re.match(mac_pattern, mac_address):
            # Check if the length is appropriate (17 characters)
            if len(mac_address) == 17:
                # Check if the number of colons (:) is correct (5 colons)
                if mac_address.count(':') == 5:
                    return True
    return False

def rs_no_next_line(command):
    if command:
        answer = rs(command)
        if answer:
            answer = answer.replace("\n", "")
        else:
            answer = False
    else:
        answer = False
    return answer

def get_router_mac_address(ip, i):
    if ip and i:
        command = "arp -n | awk '/"+ip+" / {count++; if (count == "+str(i)+") {print $3; exit}}'"
        mac_address = (rs_no_next_line(command)) 
        if mac_address_is_plausible(mac_address):
            return mac_address 
    return False

# def get_ip_router():
def get_network_info():
    network = {       
        }
    interface_default = {
        "ip_router": False,
        "ip_device": False,
        "mac_router": False,
        "mac_device": False
    }
    network.setdefault("eth0", interface_default)
    network.setdefault("wlan0", interface_default)
    for i in [1,2]:
        interface = (rs_no_next_line("ip route show default | awk '/via/ {count++} count == "+str(i)+" {print $5}'"))
        if interface:
            network[interface]["ip_router"]= (rs_no_next_line("ip route show default | awk '/via/ {count++} count == "+str(i)+" {print $3}'"))
            network[interface]["ip_device"]= (rs_no_next_line("ip route show default | awk '/via/ {count++} count == "+str(i)+" {print $9}'"))
            for j in [1,2]:
                interface_arp = (rs_no_next_line("arp -n | awk '/"+network[interface]["ip_router"]+" / {count++; if (count == "+str(j)+") {print $5; exit}}'"))
                if interface_arp and interface_arp == interface:
                    network[interface_arp]["mac_router"]= get_router_mac_address(network[interface_arp]["ip_router"], j)

    network["eth0"]["mac_device"] = params.get("eth0_MAC_address") or False
    network["wlan0"]["mac_device"] = params.get("wlan0_MAC_address") or False
    return network


def get_interface(): # returns  no internet - eth0 - wlan0
    if params.get("internetReachable") == "1":
        if on_ethernet():
            interface = "eth0"
        else:
            interface = "wlan0"
    else:
        interface = "no internet"
    params.put("router_eth_or_wlan", interface)
    return interface