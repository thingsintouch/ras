from common.logger import loggerDEBUG
import time
from common.constants import PERIOD_STATE_MANAGER, PIN_RELAY, PARAMS
from relay_state.relay_hw import Relay
from common.params import Params

params = Params(db=PARAMS)
relay = Relay(PIN_RELAY)

while True:
    params.put("relay_status", "1")
    relay.check_update_output()
    time.sleep(PERIOD_STATE_MANAGER*5)
    params.put("relay_status", "0")
    relay.check_update_output()
    time.sleep(PERIOD_STATE_MANAGER*5)