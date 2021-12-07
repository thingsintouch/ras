from time import sleep

from odoo.routineCheck import routineCheck

from common.common import get_period
from common.common import BLOCKING_waiting_until_RAS_acknowledged_from_Odoo

def main():

    BLOCKING_waiting_until_RAS_acknowledged_from_Odoo()

    while True:
        routineCheck()
        sleep(get_period("period_odoo_routine_check"))

if __name__ == "__main__":
    main()
