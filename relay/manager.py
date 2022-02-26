import time
#import zmq
#import os

from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG, loggerERROR

from messaging.messaging import SubscriberMultipart as Subscriber
#from messaging.messaging import PublisherMultipart as Publisher

from odooGetIotKeys.stored_keys import get_keys_stored
from relay.relay_switch import switch_the_relay_after_checks


def main():

    #display_publisher   = Publisher("5559")
    #buzzer_publisher    = Publisher("5558")
    odoo_subscriber     = Subscriber("5557")
    odoo_subscriber.subscribe("new_card")

    while 1:

        topic, card = odoo_subscriber.receive() # BLOCKING

        if topic == "new_card":
            keys_stored = get_keys_stored()
            NOW_in_seconds = int(time.time())
            card_as_string = f"{card}"                
            if card_as_string in keys_stored:
                expiration_date = int(keys_stored[card_as_string][0])
                if expiration_date == 0 or NOW_in_seconds < expiration_date:
                    switch_the_relay_after_checks(card_as_string, NOW_in_seconds)

        time.sleep(2)


if __name__ == "__main__":
    main()
