from reader.MFRC522 import MFRC522
from common.logger import loggerDEBUG
from common import constants as co
import time

reader = MFRC522()

while True:
    card = reader.scan_card()

    if card:
        loggerDEBUG(f"card read {card}")

    time.sleep(co.PERIOD_READER_MANAGER)