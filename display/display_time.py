from common.constants import PARAMS, DEFAULT_DISPLAY_TIME, DISPLAY_TIME_OFFSET
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR

from common.params import Params

params = Params(db=PARAMS)


def get_display_time():
    try:
        n = params.get("timeToDisplayResultAfterClocking")
        if n is None:
            # loggerDEBUG(f"No parameter stored for period_odoo_routine_check")
            display_time = DEFAULT_DISPLAY_TIME
        elif n:
            display_time = float(n) - DISPLAY_TIME_OFFSET
            if display_time < DEFAULT_DISPLAY_TIME:
                display_time = DEFAULT_DISPLAY_TIME
        else:
            display_time = DEFAULT_DISPLAY_TIME
    except Exception as e:
        loggerDEBUG(f"exception in  get_display_time: {e}")
        display_time = 1.2     
    loggerDEBUG(f"display_time {display_time} ")
    return display_time