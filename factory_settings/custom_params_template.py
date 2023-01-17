factory_settings = {
    "firmwareAtShipment"  : "3.9",
    "productName"         : "RAS2.2209",
    "productionDate"      : "20230118",
    "productionLocation"  : "Frankfurt",
    "productionNumber"    : "xxx",
    "qualityInspector"    : "LB",

    "template_to_register_device"  : "thingsintouch.ras_simplified",

    "tz"                  : "Europe/Berlin",
    "time_format"         : "12 hour",

    "hardware_machine"    : "RPi Zero W",
    "hardware_card_reader": "MFRC522",
    "hardware_display"    : "oled sh1106 - rotated",
    "hardware_sound"      : "passive buzzer",

    "card_registered"     : "REGISTERED",
    "too_little_time_between_clockings" : "TOO SOON",
    "minimumTimeBetweenClockings"       : "300",
    "period_odoo_routine_check"         : "15",  # recommended after setup: 1000s (almost 17min)
    "period_register_clockings"         : "15",   # set to 90s
    "clockings_expiration_period_in_weeks": "2", # integer between 2 an 12

    "setup_password"      : "some_password",

    "timeToDisplayResultAfterClocking"  :  "1.2",

    "shouldGetFirmwareUpdate"   : "0",
    "shutdownTerminal"          : "0",
    "rebootTerminal"            : "0",

    "partialFactoryReset"       : "0",
    "fullFactoryReset"          : "0",

    "deleteClockings"           : "0",

    "dailyRebootHour"     : "03",
    "dailyRebootMinute"   : "16",
    "automaticUpdate"     : "1",
    "RAS_runs_locally"    : "0", # "1"
}
