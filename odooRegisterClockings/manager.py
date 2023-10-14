from time import sleep
from os import listdir

from odoo.registerClockings import registerClockings, get_sorted_clockings_from_older_to_newer

from common.common import get_period
from common.common import BLOCKING_waiting_until_RAS_acknowledged_from_Odoo
from common.constants import CLOCKINGS

def main():
    get_sorted_clockings_from_older_to_newer() # delete the clockings set for deletion
    BLOCKING_waiting_until_RAS_acknowledged_from_Odoo()
    sleep(60) # wait one minute to let the cpu calm down from the reboot

    while True:
        registerClockings()
        minimum = get_period("period_register_clockings")
        clockings_waiting = len(listdir(CLOCKINGS))
        period_register_clockings = max(minimum, clockings_waiting*4)
        sleep(period_register_clockings+10)


if __name__ == "__main__":
    main()
