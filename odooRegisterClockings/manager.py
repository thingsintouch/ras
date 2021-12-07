from time import sleep

from odoo.registerClockings import registerClockings

from common.common import get_period
from common.common import BLOCKING_waiting_until_RAS_acknowledged_from_Odoo

def main():

    BLOCKING_waiting_until_RAS_acknowledged_from_Odoo()

    while True:
        registerClockings()
        sleep(get_period("period_register_clockings"))


if __name__ == "__main__":
    main()
