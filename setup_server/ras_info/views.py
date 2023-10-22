from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required

from os.path import join

from thermal.hardware_status import get_hardware_status
from odoo.odooRequests import  get_iot_template
from common.params import Params
from common.constants import PARAMS, CLOCKINGS, LAST_REGISTERED, LAST_LOGS
from common.common import get_MAC_address, return_lines_from_file, get_timestamp_human, get_network_info, get_interface
from common.common import runShellCommand_and_returnOutput as rs

from odoo.registerClockings import get_sorted_clockings_from_older_to_newer
from odoo.manager import get_two_lines_name

params = Params(db=PARAMS)

ras_info = Blueprint('ras_info',__name__)

@ras_info.route('/ras_info',methods=['GET','POST'])
@login_required
def show_info():
    (temperatureCurrent, loadAvgPerc_5min, memUsedPercent) = get_hardware_status()
    template =  get_iot_template() or "N/A"
    template = template[:-5] or "N/A"
    odoo_port_open = params.get("odooPortOpen") or "0"
    last_conn = params.get("lastConnectionWithOdoo") or "N/A"
    git_version_hash = (rs("git describe --tags")) or "N/A"
    git_repository = (rs("git remote -v")) or "N/A"
    git_repository = git_repository.split("\n")[0]
    device_name = params.get("RASxxx") or "N/A"
    wlan0_MAC_address = get_MAC_address("wlan0") or "N/A"
    eth0_MAC_address = get_MAC_address("eth0") or "N/A"
    network = get_network_info()
    print(network)
    eth0_router_MAC_address = network["eth0"]["mac_router"] or "N/A"
    eth0_router_ip = network["eth0"]["ip_router"] or "N/A"
    eth0_device_ip = network["eth0"]["ip_device"] or "N/A"
    wlan0_router_MAC_address = network["wlan0"]["mac_router"] or "N/A"
    wlan0_router_ip = network["wlan0"]["ip_router"] or "N/A"
    wlan0_device_ip = network["wlan0"]["ip_device"] or "N/A"

    # wifi_SSID = get_wifi_SSID_of_RAS()
    # wifi_success =  params.get("wifi_connection_counter_successful") or "0"
    # wifi_NO_success =  params.get("wifi_connection_counter_unsuccessful") or "0"
    return render_template('ras_info.html',
                temperatureCurrent=temperatureCurrent, 
                loadAvgPerc_5min=loadAvgPerc_5min, 
                memUsedPercent=memUsedPercent,
                template=template,
                odoo_port_open=odoo_port_open,
                last_conn=last_conn,
                git_version_hash=git_version_hash,
                git_repository=git_repository,
                device_name=device_name,
                wlan0_MAC_address=wlan0_MAC_address,
                eth0_MAC_address=eth0_MAC_address,
                eth0_router_MAC_address = eth0_router_MAC_address,
                eth0_router_ip = eth0_router_ip,
                eth0_device_ip = eth0_device_ip,
                wlan0_router_MAC_address = wlan0_router_MAC_address,
                wlan0_router_ip = wlan0_router_ip,
                wlan0_device_ip = wlan0_device_ip
                )

@ras_info.route('/show_stored_clockings',methods=['GET','POST'])
@login_required
def show_stored_clockings():
    clockings = get_sorted_clockings_from_older_to_newer()
    c_with_timestamp = []
    for c in clockings:
        timestamp_human = get_timestamp_human(timestamp_int = c[0])
        card = c[1]
        person_name = get_two_lines_name(card).replace("\n"," ")
        card_code_and_timestamp = c[2]
        with open(join(CLOCKINGS,card_code_and_timestamp), 'r') as f:
            message_from_odoo = f.readline() # .rstrip('\n')
        if not message_from_odoo: message_from_odoo = "- refer to previous clockings of this card"
        c_with_timestamp.append((timestamp_human, card, person_name, message_from_odoo))
    return render_template('show_stored_clockings.html', clockings=c_with_timestamp)

@ras_info.route('/show_registered_clockings',methods=['GET','POST'])
@login_required
def show_registered_clockings():
    clockings = return_lines_from_file(LAST_REGISTERED)
    return render_template('show_registered_clockings.html', clockings=clockings)

@ras_info.route('/show_last_logs',methods=['GET','POST'])
@login_required
def show_last_logs():
    logs = return_lines_from_file(LAST_LOGS)
    return render_template('show_last_logs.html', logs=logs)
