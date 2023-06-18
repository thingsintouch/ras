from time import sleep
from os import listdir

from odoo.registerClockings import registerClockings

from common.common import get_period
from common.common import BLOCKING_waiting_until_RAS_acknowledged_from_Odoo
from common.constants import CLOCKINGS

def main():

    BLOCKING_waiting_until_RAS_acknowledged_from_Odoo()

    while True:
        registerClockings()
        minimum = get_period("period_register_clockings")
        clockings_waiting = len(listdir(CLOCKINGS))
        period_register_clockings = max(minimum, clockings_waiting*3)
        sleep(period_register_clockings)


if __name__ == "__main__":
    main()
