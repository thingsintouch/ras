import time

from common.constants import PERIOD_STATE_MANAGER, PIN_RELAY
from relay_state.relay_hw import Relay

relay = Relay(PIN_RELAY)

def main():
    while True:
        relay.check_update_output() 
        time.sleep(PERIOD_STATE_MANAGER)

if __name__ == "__main__":
    main()
