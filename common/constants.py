from decouple import config

RAS_VERSION = "v1.4.6"
WORKING_DIR = config("WORKING_DIR")
DIR_WIFI_CONNECTIONS = config("DIR_WIFI_CONNECTIONS")
SSID_WIFICONNECT = config("SSID_WIFICONNECT")
ETH0_OPERSTATE_FILE = config("ETH0_OPERSTATE_FILE")
WLAN0_OPERSTATE_FILE = config("WLAN0_OPERSTATE_FILE")
LOG_FILE = WORKING_DIR+ "/data/ras3.log"

INTERFACES = {
    "eth0"  : [ETH0_OPERSTATE_FILE,],
    "wlan0" : [WLAN0_OPERSTATE_FILE,]
    }

PERIOD_CONNECTIVITY_MANAGER = 10 # in seconds
PERIOD_THERMAL_MANAGER = 10 # in seconds
WAIT_PERIOD_FOR_PROCESS_GRACEFUL_TERMINATION = 10 # in seconds
PERIOD_MAIN_THREAD = 10 # in seconds

MACHINE_ID_FILE = config("MACHINE_ID_FILE")
HASH_KEY = bytes(config("HASH_KEY"), encoding='utf8')
HASH_SALT = bytes(config("HASH_SALT"), encoding='utf8')
HASH_DIGEST_SIZE = int(config("HASH_DIGEST_SIZE"))
HASH_PERSON_REGISTER_TERMINAL = bytes(config("HASH_PERSON_REGISTER_TERMINAL"), encoding='utf8')

ROUTE_ACK_GATE = config("ROUTE_ACK_GATE")
ROUTE_INCOMING_IN_ODOO = config("ROUTE_INCOMING_IN_ODOO")
ROUTE_OUTGOING_IN_ODOO = config("ROUTE_OUTGOING_IN_ODOO")
ROUTE_ASK_VERSION_IN_ODOO = config("ROUTE_ASK_VERSION_IN_ODOO")

QUESTION_ASK_FOR_VERSION_IN_ODOO = config("QUESTION_ASK_FOR_VERSION_IN_ODOO")
QUESTION_ASK_FOR_ROUTINE_CHECK = config("QUESTION_ASK_FOR_ROUTINE_CHECK")
QUESTION_ASK_FOR_RESET_SETTINGS = config("QUESTION_ASK_FOR_RESET_SETTINGS")