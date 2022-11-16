import time

from common.constants import PARAMS
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
from common.params import Params
from display.helpers import Oled

from common.common import runShellCommand_and_returnOutput as rs
from common.common import get_wifi, store_wifi, connect_to_wifi_using_wpa_cli
from common.counter_ops import increase_counter

from buzzer.helpers import buzz

params = Params(db=PARAMS)
oled = Oled()

def connecting_with_wifi___visual_and_acoustic_signals():
    buzz("OK")
    wifi_network, wifi_password = get_wifi()
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
    increase_counter("wifi_connection_counter_unsuccessful")

def wifi_connection_successful():
    buzz("success_odoo_connection")
    text = f"CONNECTED\nWITH WiFi\nSUCCESSFULLY"
    loggerINFO(f"wifi_connection_successful")   
    oled.three_lines_text_small(text)
    increase_counter("wifi_connection_counter_successful")
  
def connect_process_to_wifi():
    params.put("displayClock", "no")
    connecting_with_wifi___visual_and_acoustic_signals()
    connection_successful = connect_to_wifi_using_wpa_cli()
    if connection_successful:
        wifi_connection_successful()
    else:
        wifi_connection_failed()
    time.sleep(1) 
    params.put("displayClock", "yes")
    return connection_successful

def main():   
    connect_process_to_wifi()
    return True

if __name__ == "__main__":
    main()
