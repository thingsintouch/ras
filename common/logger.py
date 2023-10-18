import logging
from systemd import journal
import time
import os

from common.constants import PARAMS, LAST_LOGS
from common.common_avoid_circularity import insert_line_at_top
from common.params import Params, Log
import re

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

def add_to_log_file(line_to_insert):
    insert_line_at_top(LAST_LOGS, line_to_insert)

def loggerDEBUG(message):
    if params.get("show_debug") is not None and params.get("show_debug")=="0":
        pass
    else:
        logger.debug(message)

def loggerINFO(message):
    add_to_log_file(time.strftime("%a, %d %b %Y %H:%M:%S ") + "INFO " + message + "\n")
    logger.info(message)

def loggerWARNING(message):
    add_to_log_file(time.strftime("%a, %d %b %Y %H:%M:%S ") + "WARNING " + message + "\n")
    logger.warning(message)

def loggerERROR(message):
    add_to_log_file(time.strftime("%a, %d %b %Y %H:%M:%S ") + "ERROR " + message + "\n")
    logger.error(message)

def loggerCRITICAL(message):
    add_to_log_file(time.strftime("%a, %d %b %Y %H:%M:%S ") + "CRITICAL " + message + "\n")
    logger.critical(message)

