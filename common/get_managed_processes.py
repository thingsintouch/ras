def get_managed_essential_processes(template):

    managed_essential_processes = { # key(=process name) : (pythonmodule where the process is defined (= process name))
        "thermal_d": "thermal.manager",
        "display_d": "display.manager",
        "clock_d": "clock.manager",
        "reader_d": "reader.manager",
        "odoo_routine_check_d": "odooRoutineCheck.manager",
        "bluetooth_d": "bluetooth.server",
        "odoo_d": "odoo.manager",
        "state_d": "state.manager",
        "buzzer_d": "buzzer.manager",
        "odoo_register_clockings_d": "odooRegisterClockings.manager"
    }

    if template == "thingsintouch.ras_plus":
        managed_essential_processes["odoo_get_iot_keys"] = "odooGetIotKeys.manager"

    return managed_essential_processes