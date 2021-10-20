import threading
import time
import json
import os
import socket
import copy
import functools
import subprocess
from datetime import datetime

from common.logger import loggerDEBUG, loggerINFO, loggerWARNING, loggerERROR, loggerCRITICAL
import odoo.odoo as od
import common.common as cc
import odoo.remoteManagement as odooRemote
import common.constants as co
from common.params import Params

params = Params(db=co.PARAMS)

WORK_DIR                      = "/home/pi/ras/"
fileDeviceCustomization       = WORK_DIR + "dicts/deviceCustomization.json"
fileDeviceCustomizationSample = WORK_DIR + "dicts/deviceCustomization.sample.json"
fileDataJson                  = WORK_DIR + "dicts/data.json"
fileCredentials               = WORK_DIR + "dicts/credentials.json"

settings                      = {}
settings_msg                  = {}
credentialsDic                = {}
defaultCredentialsDic         = {"username": ["admin"], "new password": ["admin"], "old password": ["password"]}
settingsList_And_DefaultValues = {
      'language': "ENGLISH",
      "showEmployeeName":"yes",
      "fileForMessages":"messagesDicDefault.json",
      "SSIDreset": "__RAS__",
      "odooParameters": None,
      "odooConnectedAtLeastOnce": False,
      "flask": defaultCredentialsDic,
      "timeoutToGetOdooUID": 6.0,
      "ssh": "enable",
      "sshPassword": "raspberry",
      "timeoutToCheckAttendance": 3.0,
      "periodEvaluateReachability": 5.0,
      "periodDisplayClock": 10.0,
      "timeToDisplayResultAfterClocking": 1.2,
      "terminalSetupManagement": "locally, on the terminal", # "remotely, on Odoo"
      "terminalIDinOdoo": None,
      "hashed_machine_id": None,
      "routefromOdooToDevice": None,
      "routefromDeviceToOdoo": None,
      "manufacturingData": None,
      "location": "to be defined",
      "howToDefineTime": "use +-xx:xx", # "use tz database"
      "tz_database_name": "Europe/Madrid",
      "time_format": "24 hour", # 12 hour
      "version_things_module_in_Odoo": None,
      "shouldGetFirmwareUpdate": False, # True, False
      "setRebootAt": None, # time for next reboot (not periodically - einzelfall nur)
      'shutdownTerminal': False,
      'incrementalLog': [],
      'RASxxx': '2  ',
      "installedPythonModules": [],
      "timezone": "+01:00",
      "db": None,
      "user_name": None,
      "user_password": None,
      "updateFailedCount": 0,
      "lastFirmwareUpdateTime": False,
      "lastTimeTerminalStarted": False
    }
json_liste = [
  "installedPythonModules", 
  "flask", 
  'incrementalLog',
  "odooParameters", 
  "manufacturingData", 
  "fileForMessages",
  "timeoutToGetOdooUID",
  "terminalSetupManagement",
  "terminalIDinOdoo",
  "howToDefineTime",
  "tz_database_name",
  "timezone",
  "db",
  "user_name",
  "user_password",
  "firmwareAtShipment" ,
  "productName"        ,
  "productionDate"     ,
  "productionLocation" ,
  "productionNumber"   ,
  "qualityInspector"   , 
  ]


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print("Elapsed time: {1:0.4f} seconds - Function: {0}".format(func, elapsed_time))
        return value
    return wrapper_timer

class Timer:
  def __init__(self, howLong):
    self.reset()
    self.howLong = howLong

  def reset(self):
    self.startTime = time.perf_counter()

  def elapsedTime(self):
    return (time.perf_counter()- self.startTime)

  def isElapsed(self):
    if self.elapsedTime() > self.howLong:
      return True
    return False

def returnAlwaysValidFlag(externalExitFlag = None):
  if externalExitFlag:
    exitFlag= externalExitFlag
  else:
    exitFlag = threading.Event()
    exitFlag.clear()
  
  return exitFlag

def waitUntilOneButtonIsPressed(button1, button2, externalExitFlag = None):
   
  exitFlag = returnAlwaysValidFlag(externalExitFlag)

  periodScan = 0.2 # seconds

  waitTilButtonOnePressed = threading.Thread(target=button1.threadWaitTilPressed, args=(exitFlag,periodScan,))
  waitTilButtonTwoPressed = threading.Thread(target=button2.threadWaitTilPressed, args=(exitFlag,periodScan,))

  waitTilButtonOnePressed.start()
  waitTilButtonTwoPressed.start()

  waitTilButtonOnePressed.join()
  waitTilButtonTwoPressed.join() 

def bothButtonsPressedLongEnough (button1, button2, periodCheck, howLong, externalExitFlag = None):
  
  exitFlag = returnAlwaysValidFlag(externalExitFlag)

  ourTimer = Timer(howLong)
  button1.poweron()
  button2.poweron()
  
  exitFlag.wait(periodCheck) # we have to wait, the buttons dont work inmediately after power on

  while not exitFlag.isSet():
    while button1.isPressed() and button2.isPressed():
      exitFlag.wait(periodCheck)
      if ourTimer.isElapsed():
        return True
    ourTimer.reset()

  return False # this should never happen

def setButtonsToNotPressed(button1,button2):
  if button1: button1.pressed=False
  if button2: button2.pressed=False

#@timer
def getJsonData(filePath):
  if os.path.isfile(filePath):
    try:
      with open(filePath) as f:
        data = json.load(f)
      return data  
    except Exception as e:
      loggerDEBUG(f"exception while accessing file: {filePath} -exception: {e}")
      return None
  else:
    return None

def storeJsonData(filePath,data):
  try:
    with open(filePath, 'w+') as f:
      json.dump(data,f, sort_keys=True, indent=2)
    return True
  except:
    return False

def beautifyJsonFile(filePath):
  try:
    data=getJsonData(filePath)
    storeJsonData(filePath,data)
    return True
  except:
    return False

def storeOptionInJsonFile(filePath,option,optionValue):
  data = getJsonData(filePath)
  if data:
      data[option] = optionValue
      if storeJsonData(filePath, data):
          return True
      else:
          return False
  else:
      return False

def isSuccesRunningSubprocess(command):
    try:
        completed = subprocess.run(command.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        #loggerDEBUG(f'shell command {command} - returncode: {completed.returncode}')
        if completed.returncode == 0:
            return True
        else:
            return False
    except:
        #loggerERROR(f"error - shell command: {command}")
        return False  

def isPingable(address):
  command = "ping -c 1 " + address
  return isSuccesRunningSubprocess(command)

  # response = os.system("ping -c 1 " + address)
  # if response == 0:
  #     pingstatus = True
  # else:
  #     pingstatus = False # ping returned an error
  # return pingstatus

def internetReachable():
  return isPingable("1.1.1.1")

def isIpPortOpen(ipPort): # you can not ping ports, you have to use connect_ex for ports
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.settimeout(2)
    canConnectResult = s.connect_ex(ipPort)
    if canConnectResult == 0:
      #print("Utils - IP Port OPEN ", ipPort)
      isOpen = True
    else:
      #print("Utils - IP Port CLOSED ", ipPort)
      isOpen = False
  except Exception as e:
    loggerERROR(f"Utils - exception in method isIpPortOpen: {e}")
    isOpen = False
  finally:
    s.close()
  return isOpen

def getOptionFromKey(dataDic, key):
  try:
    value = dataDic[key]
    return value
  except:
    return None

def getOptionFromDeviceCustomization(option, defaultValue):
  try:
    data = getJsonData(fileDeviceCustomization)
    value = getOptionFromKey(data,option) or defaultValue
    storeOptionInDeviceCustomization(option,value)
    return value
  except:
    return None

def storeOptionInDeviceCustomization(option,value):
  params_available = os.path.isfile(co.PARAMS_DB_TRANSFERRED_FLAG)
  try:
    if not params_available or option in json_liste:
      storeOptionInJsonFile(fileDeviceCustomization,option,value) # stores in file
    else:
      value = params.put(option, value)
    settings[option]= value # stores on the running program
    return True
  except:
    return False

def getSettingsFromDeviceCustomization():
  params_available = os.path.isfile(co.PARAMS_DB_TRANSFERRED_FLAG)

  for key, default in settingsList_And_DefaultValues.items():
    if not params_available or key in json_liste:
      value = getOptionFromDeviceCustomization(key, defaultValue = default)
    else:
      value = params.get(key, encoding='utf-8')
    loggerDEBUG(f"in getSettings... key {key} - value {value}")
    settings[key] = value

  try:
    settings["db"] = settings["odooParameters"]["db"][0]
    settings["user_name"] = settings["odooParameters"]["user_name"][0]  
    settings["user_password"] = settings["odooParameters"]["user_password"][0]
    settings["admin_id"] = settings["odooParameters"]["admin_id"][0]
    settings["timezone"] = settings["odooParameters"]["timezone"][0]
    settings["odoo_host"] = settings["odooParameters"]["odoo_host"][0]
    settings["odoo_port"] = settings["odooParameters"]["odoo_port"][0]
    if "https" in settings["odooParameters"]:
      settings["https"] = settings["odooParameters"]["https"][0]
    else:
      settings["https"] = ""
    factory_settings = [
    "firmwareAtShipment",
    "productName",
    "productionDate",
    "productionLocation",
    "productionNumber",
    "qualityInspector",
    "SSIDreset"]
    for s in factory_settings:
      settings[s] = settings["manufacturingData"][s]
  except Exception as e:
    loggerDEBUG(f"got error setting odooParameters setting (to deprecate) {e}")

  if not settings["lastFirmwareUpdateTime"]:
    settings["lastFirmwareUpdateTime"] = datetime.now().replace(microsecond=0)
  
  settings["lastTimeTerminalStarted"] = datetime.now().replace(microsecond=0)

  settings["hashed_machine_id"]   = cc.getHashedMachineId()
  settings["firmwareVersion"]     = co.RAS_VERSION
  settings["odooUrlTemplate"]     = od.setOdooUrlTemplate()
  settings["odooIpPort"]          = od.setOdooIpPort()
  settings["ownIpAddress"]        = getOwnIpAddress()
  odoo_remote_available = odooRemote.isRemoteOdooControlAvailable()
  settings["isRemoteOdooControlAvailable"] = odoo_remote_available # True or False
  if params_available:
    params.put("isRemoteOdooControlAvailable", settings["isRemoteOdooControlAvailable"])
    params.put("lastTimeTerminalStarted", str(settings["lastTimeTerminalStarted"]) )

  if not params_available:
    storeJsonData(fileDeviceCustomization,settings)

def transferDataJsonToDeviceCustomization(deviceCustomizationDic):
  dataJsonOdooParameters = getJsonData(fileDataJson)
  if dataJsonOdooParameters:
    deviceCustomizationDic["odooParameters"] = dataJsonOdooParameters
    deviceCustomizationDic["odooConnectedAtLeastOnce"] = True
  else:
    deviceCustomizationDic["odooConnectedAtLeastOnce"] = False
  return deviceCustomizationDic

def storeOdooParamsInDeviceCustomization(newOdooParams):
  try:
    storeOptionInDeviceCustomization("odooParameters",newOdooParams)
    return True
  except:
    return False

def handleMigratioOfDeviceCustomizationFile():
  '''
  if there is no "DeviceCustomization" File,
  take the sample file
  if there is a "DeviceCustomization" File,
  add the Fieldsin newOptionsList
  '''
  deviceCustomizationDic        = getJsonData(fileDeviceCustomization)
  deviceCustomizationSampleDic  = getJsonData(fileDeviceCustomizationSample)
  newOptionsList = ["SSIDreset","fileForMessages","firmwareVersion","ssh", "sshPassword", "timeoutToGetOdooUID", "timeoutToCheckAttendance", "periodEvaluateReachability", "periodDisplayClock", "timeToDisplayResultAfterClocking" ]
  if deviceCustomizationDic:
    for option in newOptionsList:
      if not(option in deviceCustomizationDic) and (option in deviceCustomizationSampleDic):
        deviceCustomizationDic[option] = deviceCustomizationSampleDic[option]
  else:
    deviceCustomizationDic = copy.deepcopy(deviceCustomizationSampleDic)
    deviceCustomizationDic = transferDataJsonToDeviceCustomization(deviceCustomizationDic)
  #print("deviceCustomizationDic: ", deviceCustomizationDic)
  storeJsonData(fileDeviceCustomization,deviceCustomizationDic)

def handleMigrationOfCredentialsJson():
  credentialsDic = getJsonData(fileCredentials)
  if not credentialsDic:
    credentialsDic = defaultCredentialsDic
  storeOptionInDeviceCustomization("flask",credentialsDic)

def migrationToVersion1_4_2():
  handleMigratioOfDeviceCustomizationFile()
  handleMigrationOfCredentialsJson()
  try:
    data = getJsonData(fileDataJson)
    loggerDEBUG(f"read dict from data.json {data}")
    if data and storeOptionInDeviceCustomization("odooParameters",data): # in data.json the Odoo Params are stored when a successful connection was made
      storeOptionInDeviceCustomization("odooConnectedAtLeastOnce", True)    
  except Exception as e:
    loggerDEBUG(f"Exception-transfer data.json to deviceCustomization file: {e}")

def isOdooUsingHTTPS():
  if not os.path.isfile(co.PARAMS_DB_TRANSFERRED_FLAG):
    if  "https" in settings["odooParameters"].keys():
      if settings["odooParameters"]["https"]== ["https"]:
        return True
    return False
  else:
    try:
      return bool(int(params.get("https", encoding='utf-8')))
    except Exception as e:
      loggerDEBUG(f"Exception- isOdooUsingHTTPS(): {e}")
      return False

  #return credentialsDic

def getOwnIpAddress():
  command = "hostname -I | awk '{ print $1}' "
  ipAddress = (subprocess.check_output(command, shell=True).decode("utf-8").strip("\n"))
  #storeOptionInDeviceCustomization("ownIpAddress",ipAddress)
  return ipAddress

def enableSSH():
  try:
    os.system("sudo systemctl enable ssh")
    os.system("sudo service ssh start")
  except Exception as e:
    loggerERROR(f"Exception in method Utils.enableSSH: {e}")

def disableSSH():
  try:
    os.system("sudo systemctl disable ssh")
    os.system("sudo service ssh stop")
  except Exception as e:
    loggerERROR(f"Exception in method Utils.disableSSH: {e}")

def isTypeOfConnection_Connected(typeConnection): # ethernet/wifi
  try:
    answer = cc.runShellCommand_and_returnOutput(
      'nmcli dev | grep '+ typeConnection +' | grep -w "connected"')
    if answer:
      return True
    else:
      return False
  except Exception as e:
    #loggerERROR(f'Exception while checking if type of connection {typeConnection} is connected: {e}')
    return False
    

def removeMessagesFromDeviceCustomizationJson():
    try:
        m1 = settings.pop("messagesDic", None)
        m2 = settings.pop("defaultMessagesDic", None)
        if m1 or m2:
            storeJsonData(fileDeviceCustomization,settings)
            storeJsonData(fileDeviceCustomizationSample,settings)
    except Exception as e:
        loggerERROR(f'Exception in Utils.removeMessagesFromDeviceCustomizationJson: {e}')