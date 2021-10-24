import logging
from systemd import journal
import time
import os

from common.constants import PARAMS
from common.params import Params, Log
import re
from datetime import datetime

params = Params(db=PARAMS)
log_db =  Log()

logger = logging.getLogger('ras')

logger.setLevel(logging.DEBUG) 

formatter = logging.Formatter('%(asctime)s %(name)s %(processName)s %(levelname)s: %(message)s')

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)
consoleHandler.setFormatter(formatter)

logger.addHandler(journal.JournalHandler())


def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def appendToIncrementalLog(message):
    message = escape_ansi(message)
    log_db.put(message)

    # currentLog = params.get("incrementalLog")
    # if currentLog:
    #     currentLog = currentLog + "\n" + message
    # else:
    #     currentLog = message
    # params.put("incrementalLog", currentLog)

def loggerDEBUG(message):
    logger.debug(message)

def loggerINFO(message):
    appendToIncrementalLog(datetime.utcnow() + "UTC -INFO " + message)
    logger.info(message)

def loggerWARNING(message):
    appendToIncrementalLog(datetime.utcnow() + "UTC -WARNING " + message)
    logger.warning(message)

def loggerERROR(message):
    appendToIncrementalLog(datetime.utcnow() + "UTC -ERROR " + message)
    logger.error(message)

def loggerCRITICAL(message):
    appendToIncrementalLog(datetime.utcnow() + "UTC -CRITICAL " + message)
    logger.critical(message)

