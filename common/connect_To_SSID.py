import time

from common.constants import PARAMS
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.params import Params
from display.helpers import Oled

from common.common import runShellCommand_and_returnOutput as rs
from common.counter_ops import increase_counter

from buzzer.helpers import buzz

params = Params(db=PARAMS)
oled = Oled()

def store_RAS_WiFi_connection_as_RAS_temp():
    try:
        rs('sudo nmcli c modify "RAS" connection.id "RAS_temp"')
    except Exception as e:
        loggerDEBUG(f"store_RAS____WiFi_connection_as____RAS_temp - Exception: {e}")

def delete_RAS_temp_WiFi_connection():
    try:
        rs('sudo nmcli c delete "RAS_temp"')
    except Exception as e:
        loggerDEBUG(f"delete_RAS_temp____WiFi_connection- Exception: {e}")

def delete_RAS_WiFi_connection():
    try:
        rs('sudo nmcli c delete "RAS"')
    except Exception as e:
        loggerDEBUG(f"delete_RAS_____WiFi_connection- Exception: {e}")

def retrieve_RAS_temp_and_make_it_to_main_RAS_WiFi_connection():
    try:
        rs('sudo nmcli c modify "RAS_temp" connection.id "RAS"')
        rs('sudo nmcli c up "RAS"')
    except Exception as e:
        loggerDEBUG(f"retrieve_RAS_temp_and_make_it_to_main_RAS_WiFi_connection- Exception: {e}")

def manage_wifi_network_name_with_spaces(wifi_network):
    if " " in wifi_network:
        wifi_network_for_cli_command = "'" + wifi_network + "'"
    else:
        wifi_network_for_cli_command = wifi_network
    return wifi_network_for_cli_command

def connecting_with_wifi___visual_and_acoustic_signals(wifi_network):
    buzz("OK")
    text = f"CONNECTING\nWITH WiFi\n{wifi_network}"
    oled.three_lines_text_small(text)

def would_be_duplicated_connection(wifi_network, wifi_password):
    wifi_network_stored = params.get("wifi_network") or False
    if wifi_network_stored and wifi_network_stored==wifi_network:
        wifi_password_stored = params.get("wifi_password") or False
        if wifi_password_stored and wifi_password_stored==wifi_password:
            return True     
    return False

def wifi_connection_failed():
    buzz("failed_odoo_connection")
    text = f"NO CONNECTION\nWITH THE\nWiFi"
    oled.three_lines_text_small(text)
    delete_RAS_WiFi_connection()
    retrieve_RAS_temp_and_make_it_to_main_RAS_WiFi_connection()
    increase_counter("wifi_connection_counter_unsuccessful")

def wifi_connection_successful(wifi_network, wifi_password):
    buzz("success_odoo_connection")
    text = f"CONNECTED\nWITH WiFi\nSUCCESSFULLY"
    loggerINFO(f"Connected to Internet - WiFi Network: {wifi_network}")   
    params.put("wifi_network", wifi_network)
    params.put("wifi_password", wifi_password)
    oled.three_lines_text_small(text)
    delete_RAS_temp_WiFi_connection()
    increase_counter("wifi_connection_counter_successful")

# def disconnect_ethernet(): # nmcli dev disconnect eth0 - nmcli c down eth0
#     answer = (rs('sudo nmcli c down "Wired connection 1"'))
#     time.sleep(2) 

# def reconnect_ethernet():
#     answer = (rs('sudo nmcli c up "Wired connection 1"'))

def connect_to_new_wifi_network(wifi_network, wifi_password):
    connecting_with_wifi___visual_and_acoustic_signals(wifi_network)
    store_RAS_WiFi_connection_as_RAS_temp() # if the new WiFi connection does not work we have the old one still
    wifi_network_for_cli_command = manage_wifi_network_name_with_spaces(wifi_network)
    answer = (rs('sudo nmcli dev wifi con '+wifi_network_for_cli_command+' password '+wifi_password+' name "RAS"'))
    connection_successful= False
    try:
        if "successfully activated" in answer:
            connection_successful= True
    except Exception as e:
        loggerDEBUG(f"Exception while connecting to WiFi network: {e}")
    return connection_successful

def connect_process_to_wifi(wifi_network, wifi_password):
    #disconnect_ethernet()
    connection_successful= connect_to_new_wifi_network(wifi_network, wifi_password) 
    #reconnect_ethernet()
    return connection_successful

def main(wifi_network, wifi_password):
    #store_RAS_WiFi_connection_as_RAS_temp()
    params.put("wifi_network", wifi_network)
    params.put("wifi_password", wifi_password)
    delete_RAS_WiFi_connection()    
    wifi_network_for_cli_command = manage_wifi_network_name_with_spaces(wifi_network)
    answer = (rs('sudo nmcli c add type wifi ssid '+wifi_network_for_cli_command+' ifname wlan0 con-name "RAS" wifi-sec.psk '+wifi_password))
    return True

if __name__ == "__main__":
    main()
