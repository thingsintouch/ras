import time
import zmq

from common import constants as co
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
#from messaging.messaging import PublisherMultipart as Publisher
from messaging.messaging import SubscriberMultipart as Subscriber

from display.helpers import Oled

from common.params import Params

params = Params(db=co.PARAMS)


def main():

    def get_display_time():
        try:
            n = params.get("timeToDisplayResultAfterClocking")
            if n is None:
                # loggerDEBUG(f"No parameter stored for period_odoo_routine_check")
                display_time = co.DEFAULT_DISPLAY_TIME
            elif n:
                display_time = float(n) - co.DISPLAY_TIME_OFFSET
                if display_time < co.DEFAULT_DISPLAY_TIME:
                    display_time = co.DEFAULT_DISPLAY_TIME
            else:
                display_time = co.DEFAULT_DISPLAY_TIME
        except Exception as e:
            loggerDEBUG(f"exception in  get_display_time: {e}")
            display_time = 1.2     
        loggerDEBUG(f"display_time {display_time} ")
        return display_time


    display_subscriber = Subscriber("5559")
    display_subscriber.subscribe("display_card_related_message")
    display_subscriber.subscribe("display_control")    

    oled = Oled()
    
    while 1:
        # get 
        topic, message = display_subscriber.receive() # BLOCKING
        #loggerDEBUG(f"received {topic} {message}")
        if topic == "display_card_related_message":
            params.put("displayClock", "no")
            # , load = \
            #     message.split()
            text = f"new message on display: \n {message}"
            loggerDEBUG(text)           
            oled.three_lines_text(message)
            time.sleep(get_display_time())

        time.sleep(co.PERIOD_DISPLAY_MANAGER)
        params.put("displayClock", "yes")

if __name__ == "__main__":
    main()
