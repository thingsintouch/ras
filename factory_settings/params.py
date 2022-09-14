factory_settings = {
    "firmwareAtShipment"  : "3.7-oca",
    "productName"         : "RAS2.2208-OCA",
    "productionDate"      : "20220818",
    "productionLocation"  : "Frankfurt",
    "productionNumber"    : "001",
    "qualityInspector"    : "Luis",

    "template_to_register_device"  : "thingsintouch.ras_simplified",  # thingsintouch.ras

    "tz"                  : "Europe/Madrid",
    "time_format"         : "12 hour", # "24 hour"

    "hardware_machine"    : "RPi Zero W",
    "hardware_card_reader": "MFRC522",
    "hardware_display"    : "oled sh1106 - rotated", # "oled sh1106"
    "hardware_sound"      : "passive buzzer",

    "card_registered"                   : "REGISTERED",
    "too_little_time_between_clockings" : "TOO SOON",
    "minimumTimeBetweenClockings"       : "300",
    "period_odoo_routine_check"         : "15",  # recommended after setup: 1000s (almost 17min)
    "period_register_clockings"         : "15",   # set to 90s
    "clockings_expiration_period_in_weeks": "2", # integer between 2 an 12

    "setup_password"                    : "some_password",

    "timeToDisplayResultAfterClocking"  :  "1.2",

    "shouldGetFirmwareUpdate"   : "0",
    "shutdownTerminal"          : "0",
    "rebootTerminal"            : "0",

    "partialFactoryReset"       : "0",
    "fullFactoryReset"          : "0",

    "deleteClockings"           : "0",
    
    "odooUrlTemplate"     : "https://example.com:9110",
    "odoo_host"           : "example.com",
    "odoo_port"           : "9110",
    "dailyRebootHour"     : "03",
    "dailyRebootMinute"   : "16",
    "automaticUpdate"     : "1",  
    "RAS_runs_locally"    : "0", # "1"
}
