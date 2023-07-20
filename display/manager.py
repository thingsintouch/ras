import time
#import zmq

from common.constants import PARAMS, PERIOD_DISPLAY_MANAGER
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR
#from messaging.messaging import PublisherMultipart as Publisher
from messaging.messaging import SubscriberMultipart as Subscriber

from display.helpers import Oled
from display.display_time import get_display_time

from common.params import Params

params = Params(db=PARAMS)


def main():

    display_subscriber = Subscriber("5559")
    display_subscriber.subscribe("display_card_related_message")
    display_subscriber.subscribe("display_control")    

    oled = Oled()
    
    while 1:
        topic, message = display_subscriber.receive() # BLOCKING
        if topic == "display_card_related_message":
            loggerINFO(f"received {topic} {message}")
            params.put("displayClock", "no")
            time.sleep(0.3) # give time the screen to change
            text = f"new message on display: \n {message}"
            #loggerDEBUG(text)           
            oled.three_lines_text(message)
            display_time = max(0.1, get_display_time()-1.2)
            time.sleep(display_time)

        time.sleep(PERIOD_DISPLAY_MANAGER)
        params.put("displayClock", "yes")

if __name__ == "__main__":
    main()
