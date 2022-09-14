import time
import zmq

from common.constants import PERIOD_THERMAL_MANAGER
from messaging.messaging import PublisherMultipart as Publisher
from thermal.hardware_status import get_hardware_status

def main():
    pub_thermal = Publisher("5556")
    while True:
        (temperatureCurrent, loadAvgPerc_5min, memUsedPercent) = get_hardware_status()
        message = f"{temperatureCurrent} {loadAvgPerc_5min} {memUsedPercent}"
        pub_thermal.publish("thermal", message)
        # temperature max CPU RPi 85°C - Yellow > 80°C - Red > 84°C (self defined limits)
        time.sleep(PERIOD_THERMAL_MANAGER)

if __name__ == "__main__":
    main()
