import time
from common.constants import PERIOD_STATE_MANAGER, PARAMS
from common.params import Params
from common.connectivity import reconnect_to_wifi

params = Params(db=PARAMS)

params.put("internetReachable", "0")
params.put("wifi_network", "FRITZ!Box 6490 Cable")
params.put("wifi_password", "52296826201105661806")
c = 0
while True:
    counter = params.get("counter_wifi_disconnected")
    print(f"iteration:{c} - counter:{counter} ")
    c = c+1
    reconnect_to_wifi() # RPi tends to disconnect itself from time to time
    time.sleep(PERIOD_STATE_MANAGER)    