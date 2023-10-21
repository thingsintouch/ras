from enum import Enum, auto


class TxType(Enum): 
    FACTORY_SETTINGS            = auto()  # will never change
    FACTORY_DEFAULT_VALUES      = auto()  # default values (pre-settings)
    ON_DEVICE_SETUP             = auto()  # parameters are defined on device setup
    ON_ACK_FROM_ODOO            = auto()
    ON_REGISTERING_FROM_DEVICE  = auto()
    ON_ROUTINE_CALLS            = auto()  # Updates come from Odoo - do not clear on start,
    FLAG                        = auto()  # used as flag in the firmware
    LOG                         = auto()  # key to store the logs
    DISPLAY_MESSAGE             = auto()  # which message will be displayed
    RFID_CARD_CODE              = auto()
    ON_SETUP_SERVER             = auto()

keys_by_Type = {}

keys_by_Type[TxType.DISPLAY_MESSAGE] = [
    "card_registered",
    "too_little_time_between_clockings",
    "check_in_message_display",
    "check_out_message_display"
    ]

keys_by_Type[TxType.ON_ROUTINE_CALLS] =     \
    keys_by_Type[TxType.DISPLAY_MESSAGE] + [

    "setup_password",

    "tz",
    "time_format",

    "minimumTimeBetweenClockings",

    "period_odoo_routine_check",
    "period_register_clockings",
    "period_odoo_get_iot_keys",
    
    "timeToDisplayResultAfterClocking",

    "shouldGetFirmwareUpdate",
    "shutdownTerminal",
    "rebootTerminal",

    "partialFactoryReset", # do not delete locally stored clocking data
    "fullFactoryReset",    # will delete locally stored clocking data
    "RASxxx",
    "show_debug",
    "emailLogs",
    "send_emailLogs",
    "smtp_password",
    "setEthernetMAC",
    "deleteIPs",
    "delete_clockings_not_recognized"
    
    ] 


keys_by_Type[TxType.FACTORY_DEFAULT_VALUES]  = \
    keys_by_Type[TxType.ON_ROUTINE_CALLS] + [

    "odooUrlTemplate",
    "odoo_host",
    "odoo_port",
    "dailyRebootHour",
    "dailyRebootMinute",
    "automaticUpdate"
    ]

keys_by_Type[TxType.FACTORY_SETTINGS] = [
    "firmwareAtShipment",
    "productName"       ,
    "productionDate"    ,
    "productionLocation",
    "productionNumber"  ,
    "qualityInspector"  , 

    "ordered_by",
    "invoice_nr",

    "hardware_machine",
    "hardware_card_reader",
    "hardware_display",
    "hardware_sound",
    "template_to_register_device",
    "use_self_generated_eth0_MAC_address"

  ]

keys_by_Type[TxType.ON_DEVICE_SETUP] = [
    "https",
    "odoo_host",
    "odoo_port",
    "odooConnectedAtLeastOnce",
    "odooUrlTemplate",
    "hasCompletedSetup",
    "bluetooth_device_name",

    "serial_sync",
    "passphrase_sync",

    "serial_async",
    "passphrase_async",

    "serial_routine",
    "passphrase_routine",

    "serial_call_lock_sync",
    "passphrase_call_lock_sync",

    "serial_call_lock_async",
    "passphrase_call_lock_async",

    "serial_get_iot_keys",
    "passphrase_get_iot_keys",
    "eth0_MAC_address",
    "wlan0_MAC_address"
  ]

keys_by_Type[TxType.ON_ACK_FROM_ODOO] = [
    #"terminalIDinOdoo",
    #"id",
    "RASxxx",
    #"routefromDeviceToOdoo",
    #"routefromOdooToDevice",
    "version_things_module_in_Odoo",
    "minimumTimeBetweenClockings"     , # in seconds
    "period_odoo_routine_check", # in seconds
    "timeToDisplayResultAfterClocking",
    "firmwareVersion",
  ]

keys_by_Type[TxType.ON_REGISTERING_FROM_DEVICE] = [
    "ip",
    #"lastFirmwareUpdateTime",
    #"lastTimeTerminalStarted",
    #"updateFailedCount",
    "hashed_machine_id",
    "setup_password",
  ]

keys_by_Type[TxType.ON_SETUP_SERVER] = [
    "odooUrlTemplate",
    "odoo_host",
    "odoo_port",
    "template_to_register_device",
    "RAS_runs_locally",
    "clockings_expiration_period_in_weeks",
    "show_checkin_or_out_display",
    "use_self_generated_eth0_MAC_address"
    ]

keys_by_Type.update({
  TxType.FLAG:
    [
      "displayClock",
      "acknowledged",
      "isRemoteOdooControlAvailable",
      "internetReachable",
      "odooPortOpen",
      "thermalMessageCounter",
      'lastLogMessage',
      "relay_status",
      "last_relay_action",
      "dependencies_v3_7",
      "automaticUpdate",
      "lastConnectionWithOdoo",
      "counter_wifi_disconnected",
      "wifi_network",
      "wifi_password",
      "wifi_connection_counter_successful",
      "wifi_connection_counter_unsuccessful",
      "RAS_runs_locally",
      "deleteClockings"
    ]
  })

keys_by_Type.update({
  TxType.LOG:
    [
      "incrementalLog",
    ]
  })

keys = {}

for e in TxType:
  if e in keys_by_Type.keys():
    for k in keys_by_Type[e]:
      #print(f"key: {k} and value: {e} - {e.value}")
      if keys.get(k, None) is None:
        keys[k]=[e.value]
      else:
        existing = keys[k]
        existing.append(e.value)
        keys[k] = existing

keys_routine_calls={}

"""
Candidates for Routine Calls #################################################
      "ssh"                             ,
      "showEmployeeName"                ,
      "sshPassword"                     ,
      "language"                        ,
      "timeoutToCheckAttendance"        ,  
      "periodEvaluateReachability"      ,
      "periodDisplayClock"              ,
      "location"                        ,
      "setRebootAt"                     , # time for next reboot (not periodically, one time reboot)
      "gitBranch"                       ,
      "gitCommit"                       ,
      "gitRemote"                       ,
      "updateOTAcommand"                ,
      "doFactoryReset"                  ,
      "updateAvailable"                 , # to be proofed in Odoo every day @03:00 + random
      "lastConnectionOdooTerminal"      ,
      "periodCPUtemperatureLOGS"        , # in minutes

"""