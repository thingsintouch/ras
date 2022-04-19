#! /usr/bin/python3.7

import os, sys, time 
import importlib
from multiprocessing import Process, Manager

from typing import Dict, List

import zmq
from colorama import Fore as cf

from common import constants as co
from common.params import Params
from common.launcher import launcher
from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
from messaging.messaging import SubscriberMultipart as Subscriber
from common.common import setTimeZone, store_hashed_machine_id, store_factory_settings_in_database
from common.common import set_bluetooth_device_name, ensure_git_does_not_change_env_file, get_own_IP_address
from common.common import runShellCommand_and_returnOutput as rs


params = Params(db=co.PARAMS)

params.put("acknowledged", "0") # terminal is NOT acknowledged at the beginning
store_factory_settings_in_database()
setTimeZone()

loggerINFO("###################### RAS launched ###################")
# loggerINFO(f'running on python version: {sys.version}')

store_hashed_machine_id()
# set_bluetooth_device_name()
params.put("firmwareVersion",co.RAS_VERSION)
ensure_git_does_not_change_env_file()
params.put("ownIpAddress", get_own_IP_address())

# MANUAL EDITIONS
# params.put("odooUrlTemplate", "http://192.168.178.55:9100")
# params.put("odoo_host", "192.168.178.55")
# params.put("odoo_port", "9100")

managed_processes = { # key(=process name) : (pythonmodule where the process is defined (= process name))
    "thermal_d": "thermal.manager",
    "display_d": "display.manager",
    "clock_d": "clock.manager",
    "reader_d": "reader.manager",
    "odoo_routine_check_d": "odooRoutineCheck.manager",
    #"bluetooth_d": "bluetooth.server",
    "odoo_d": "odoo.manager",
    "state_d": "state.manager",
    "buzzer_d": "buzzer.manager",
    "odoo_register_clockings_d": "odooRegisterClockings.manager"
    #"RAS_d": "oldLauncher"
}

running: Dict[str, Process] = {}

def start_managed_process(name):
    if name not in running and name in managed_processes:
        preimport_managed_process(name)
        process = managed_processes[name]
        loggerINFO(f"starting python process {process}")
        running[name] = Process(name=name, target=launcher, args=(process,))
        running[name].start()


def preimport_managed_process(name):
    module = managed_processes[name]
    loggerDEBUG(f"preimporting {module}")
    importlib.import_module(module)

def start_all_managed_processes():
    for name in managed_processes:
        start_managed_process(name)

def log_running_processes_list():
    running_alive = [p for p in running if running[p].is_alive()]
    running_dead = [p for p in running if p not in running_alive]
    if running_dead:
        loggerINFO("alive processes: " + cf.GREEN + ' ; '.join(running_alive) + cf.RESET)    
        loggerINFO("dead processes: " + cf.RED + ' ; '.join(running_dead) + cf.RESET)

def manager_thread():
    def get_thermal_status(counter):
        def log_info_when_needed(counter):
            try:
                period_between_logs = int(params.get("periodCPUtemperatureLOGS")) * 60
            except:
                period_between_logs = 360

            if counter*co.PERIOD_MAIN_THREAD > period_between_logs:
                loggerINFO(f"thermal update - T {temperature}°C," + \
                    f" CPU load (5 minutes avg) {load_5min}%, mem used {memUsed}%")
                counter = 0
            return counter

        topic, message = ras_subscriber.receive() # BLOCKING
        #loggerDEBUG(f"received {topic} {message}")
        #loggerDEBUG(f"thermal status counter {counter}")
        if topic == "thermal":
            temperature, load_5min, memUsed = \
                message.split()
            counter = log_info_when_needed(counter)
        return counter 


    ras_subscriber = Subscriber("5556")
    ras_subscriber.subscribe("thermal")

    start_all_managed_processes()

    counter = 0
    while 1:
        counter = get_thermal_status(counter) # BLOCKING

        start_all_managed_processes()

        log_running_processes_list()
        time.sleep(co.PERIOD_MAIN_THREAD)
        counter += 1


def main():

  try:
    manager_thread()
  except Exception as e:
    loggerCRITICAL(f'managerThread() failed to start with exception {e}')
  finally:
    # TODO cleanupAllProcesses()
    pass


if __name__ == "__main__":

  try:
    main()
  except Exception as e:
    loggerCRITICAL(f'main() failed to start with exception {e}')
