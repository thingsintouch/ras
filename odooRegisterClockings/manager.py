from time import sleep
from os import listdir

from odoo.registerClockings import registerClockings, get_sorted_clockings_from_older_to_newer

from common.common import get_period
from common.common import BLOCKING_waiting_until_RAS_acknowledged_from_Odoo
from common.constants import CLOCKINGS
from common.logger import loggerERROR
import traceback

def main():
    sleep(60) # wait one minute to let the cpu calm down from the reboot
    BLOCKING_waiting_until_RAS_acknowledged_from_Odoo()
    try:
        get_sorted_clockings_from_older_to_newer() # delete the clockings set for deletion
    except Exception as e:
        loggerERROR(f"on process register_clockings_process before the main loop - trying to delete old clockings and sort the remaining ones - exception {e}")

    while True:
        try:
            registerClockings()
            minimum = get_period("period_register_clockings")
            clockings_waiting = len(listdir(CLOCKINGS))
            period_register_clockings = max(minimum, clockings_waiting*4)
            sleep(period_register_clockings+10)
        except Exception as e:
            traceback_info = traceback.format_exc()
            loggerERROR(f"on main loop of register_clockings_process - exception {e}")
            loggerERROR(traceback_info)
            sleep(10)


if __name__ == "__main__":
    main()
