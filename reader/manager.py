import time

from common import constants as co
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG
from messaging.messaging import PublisherMultipart as Publisher
from common.params import Params
from common.common import runShellCommand_and_returnOutput as rs

params = Params(db=co.PARAMS)


def get_scan_reader_function():
    # scan_function = {}
    # scan_function
    try:
        hardware_card_reader = params.get("hardware_card_reader")
    except Exception as e:
        loggerDEBUG(f"did not found a 'hardware card reader' on the parameters: {e}")
        hardware_card_reader = "MFRC522" # default

    loggerDEBUG(f"Reader is: {hardware_card_reader}")

    if hardware_card_reader == "RDM6300":
        from reader.RDM6300 import scan_card
        rs("sudo systemctl stop serial-getty@ttyS0.service")
        rs("sudo systemctl disable serial-getty@ttyS0.service")
        return scan_card

    from reader.MFRC522 import MFRC522
    reader = MFRC522()
    return reader.scan_card # default option

def main():

    new_card_publisher = Publisher("5557")

    #reader = MFRC522()
    scan_function = get_scan_reader_function()

    while True:
        #card = reader.scan_card()
        card = scan_function()

        if card:
            loggerDEBUG(f"card read {card}")

            card_id_as_string = f"{card}"

            new_card_publisher.publish("new_card", card_id_as_string)

        time.sleep(co.PERIOD_READER_MANAGER)


if __name__ == "__main__":
    main()