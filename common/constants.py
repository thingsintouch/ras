from decouple import config

RAS_VERSION = "3.8"
WORKING_DIR = config("WORKING_DIR")

PERIOD_CONNECTIVITY_MANAGER = 10 # in seconds
PERIOD_THERMAL_MANAGER = 360 # in seconds
PERIOD_DISPLAY_MANAGER = 0.8 # in seconds
PERIOD_CLOCK_MANAGER = 0.7 # in seconds
PERIOD_READER_MANAGER = 0.6 # in seconds
PERIOD_STATE_MANAGER = 3 # in seconds
PERIOD_ACK_STATE_MANAGER = 1 # in seconds
PERIOD_BUZZER_MANAGER = 0.5 # in seconds

CYCLES_OF_STATE_MANAGER_TO_WAIT_FOR_WIFI_RECONNECTION_ATTEMPT = 60 

DEFAULT_MINIMUM_PERIOD = 14 # in seconds
# PERIOD_ODOO_REGISTER_CLOCKINGS = 10 # in seconds
WAIT_PERIOD_FOR_PROCESS_GRACEFUL_TERMINATION = 10 # in seconds
PERIOD_MAIN_THREAD = 10 # in seconds

DEFAULT_MINIMUM_TIME_BETWEEN_CLOCKINGS = 60  # in seconds
DEFAULT_DISPLAY_TIME = 1.2 # in seconds
DISPLAY_TIME_OFFSET = 0.7 # in seconds
MINIMUM_TIME_BETWEEN_RELAY_SWITCHINGS = 5 # in seconds

MACHINE_ID_FILE = config("MACHINE_ID_FILE")
HASH_KEY = bytes(config("HASH_KEY"), encoding='utf8')
HASH_SALT = bytes(config("HASH_SALT"), encoding='utf8')
HASH_DIGEST_SIZE = int(config("HASH_DIGEST_SIZE"))
HASH_PERSON_REGISTER_TERMINAL = bytes(config("HASH_PERSON_REGISTER_TERMINAL"), encoding='utf8')

PARAMS = WORKING_DIR + "/data/params"
LAST_REGISTERED = WORKING_DIR + "/data/last_registered.txt"
CLOCKINGS = WORKING_DIR + "/data/clockings"
IN_OR_OUT = WORKING_DIR + "/data/in_or_out"
LOG = WORKING_DIR + "/data/log"
KEYS = WORKING_DIR + "/data/keys"
KEY_ACTIONS = WORKING_DIR + "/data/key_actions"
ETHERNET_FLAG_FILE = "/sys/class/net/eth0/carrier" # if 1, ethernet is up


MAX_NUMBER_OF_LOG_ENTRIES = 100

PIN_RELAY = 29

