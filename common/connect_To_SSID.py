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
    rs('sudo nmcli c modify "RAS" connection.id "RAS_temp"')

def delete_RAS_temp_WiFi_connection():
    rs('sudo nmcli c delete "RAS_temp"')

def delete_RAS_WiFi_connection():
    rs('sudo nmcli c delete "RAS"')

def retrieve_RAS_temp_and_make_it_to_main_RAS_WiFi_connection():
    rs('sudo nmcli c modify "RAS_temp" connection.id "RAS"')
    rs('sudo nmcli c up "RAS"')

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

def main(wifi_network, wifi_password):
    if not would_be_duplicated_connection(wifi_network, wifi_password):
        params.put("displayClock", "no")
        connecting_with_wifi___visual_and_acoustic_signals(wifi_network)
        store_RAS_WiFi_connection_as_RAS_temp() # if the new WiFi connection does not work we have the old one still
        wifi_network_for_cli_command = manage_wifi_network_name_with_spaces(wifi_network)
        answer = (rs('sudo nmcli dev wifi con '+wifi_network_for_cli_command+' password '+wifi_password+' name "RAS"'))
        if "successfully activated" in answer:
            buzz("success_odoo_connection")
            text = f"CONNECTED\nWITH WiFi\nSUCCESSFULLY"
            loggerINFO(f"Connected to Internet - WiFi Network: {wifi_network}")
            connection_successful= True
            params.put("wifi_network", wifi_network)
            params.put("wifi_password", wifi_password)
            oled.three_lines_text_small(text)
            delete_RAS_temp_WiFi_connection()
            increase_counter("wifi_connection_counter_successful")
        else:
            buzz("failed_odoo_connection")
            text = f"NO CONNECTION\nWITH THE\nWiFi"
            oled.three_lines_text_small(text)
            delete_RAS_WiFi_connection()
            retrieve_RAS_temp_and_make_it_to_main_RAS_WiFi_connection()
            increase_counter("wifi_connection_counter_unsuccessful")
            connection_successful= False
        time.sleep(1) 
        params.put("displayClock", "yes")
    else:
        connection_successful= True
    return connection_successful or False


if __name__ == "__main__":
    main()