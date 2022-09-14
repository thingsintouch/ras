def get_managed_essential_processes(template):

    managed_essential_processes = { # key(=process name) : (pythonmodule where the process is defined (= process name))
        "thermal_d": "thermal.manager",
        "display_d": "display.manager",
        "clock_d": "clock.manager",
        "reader_d": "reader.manager",        
        "bluetooth_d": "bluetooth.server",
        "odoo_d": "odoo.manager",
        "state_d": "state.manager",
        "buzzer_d": "buzzer.manager",
        "odoo_register_clockings_d": "odooRegisterClockings.manager",
        "setup_server_d": "setup_server.server"
    }

    if template == "thingsintouch.ras_simplified":
        return managed_essential_processes

    if template == "thingsintouch.ras_plus":
        managed_essential_processes["odoo_get_iot_keys_d"] = "odooGetIotKeys.manager"
        managed_essential_processes["relay_d"] = "relay.manager"
        managed_essential_processes["relay_output_d"] = "relay_state.manager"
        managed_essential_processes["odoo_register_actions_d"] = "odooRegisterActions.manager"
        managed_essential_processes["odoo_routine_check_d"] = "odooRoutineCheck.manager"
        return managed_essential_processes

    if template == "thingsintouch.ras":
        managed_essential_processes["odoo_routine_check_d"] = "odooRoutineCheck.manager"
        return managed_essential_processes

    
    managed_essential_processes["odoo_routine_check_d"] = "odooRoutineCheck.manager"
    return managed_essential_processes
