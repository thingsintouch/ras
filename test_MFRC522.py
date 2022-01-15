import time

from common import constants as co
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG

from common.params import Params

params = Params(db=co.PARAMS)

from reader.MFRC522 import MFRC522

reader = MFRC522()

while True:
    card = reader.scan_card()

    if card:
        loggerDEBUG(f"card read {card}")

        # card_id_as_string = f"{card}"

        # new_card_publisher.publish("new_card", card_id_as_string)

    time.sleep(co.PERIOD_READER_MANAGER)
