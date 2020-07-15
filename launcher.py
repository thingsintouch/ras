#! /usr/bin/python3.5
import os
import time
import logging
import logging.handlers

format = "%(asctime)s %(pid)s %(levelname)s %(name)s: %(message)s"

from dicts.ras_dic import PinsBuzzer, PinsDown, PinsOK
from lib import Display, CardReader, PasBuz, Button
from lib import OdooXMLrpc, Tasks

import traceback
from io import StringIO


_logger = logging.getLogger(__name__)

Buzz = PasBuz.PasBuz(PinsBuzzer)
Disp = Display.Display()
Reader = CardReader.CardReader()
B_Down = Button.Button(PinsDown)
B_OK = Button.Button(PinsOK)
Hardware = [Buzz, Disp, Reader, B_Down, B_OK]

Odoo = OdooXMLrpc.OdooXMLrpc()  
Tasks = Tasks.Tasks(Odoo, Hardware)

def mainLoop():
    try:
        Disp.displayGreetings()

        Tasks.ensureThatWifiWorks()
        
        Tasks.ensureThatOdooHasBeenReachedAtLeastOnce() 

        Tasks.nextTask = "clocking"

        Buzz.Play("OK")

        while True:

            if Tasks.nextTask:
                Tasks.executeNextTask()
            else:
                Tasks.chooseTaskFromMenu()


    except Exception as e:
        buff = StringIO()
        traceback.print_exc(file=buff)
        _logger.error(buff.getvalue())
        raise e


class RASFormatter(logging.Formatter):
    def format(self, record):
        record.pid = os.getpid()
        return logging.Formatter.format(self, record)

log_file = '/var/log/ras.log'

if not os.path.isfile(log_file):
    os.system("sudo touch "+log_file)

os.system("sudo chmod 777 "+log_file)

handler = logging.handlers.TimedRotatingFileHandler(
    filename = log_file, when="D", interval=1, backupCount=30
)

handler.setFormatter(RASFormatter(format))
logging.getLogger().addHandler(handler)

mainLoop()
