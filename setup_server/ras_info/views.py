from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required

from thermal.hardware_status import get_hardware_status
from odoo.odooRequests import  get_iot_template
from common.params import Params
from common.constants import PARAMS
from common.common import runShellCommand_and_returnOutput as rs
#from common.common import get_wifi_SSID_of_RAS

from odoo.registerClockings import get_sorted_clockings_from_older_to_newer
from odoo.manager import get_two_lines_name
from datetime import datetime
import pytz

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
                # wifi_SSID=wifi_SSID,
                # wifi_success=wifi_success,
                # wifi_NO_success=wifi_NO_success
                )

@ras_info.route('/show_stored_clockings',methods=['GET','POST'])
@login_required
def show_stored_clockings():
    clockings = get_sorted_clockings_from_older_to_newer()
    tz = params.get("tz") or "Europe/Berlin"
    tzinfo = pytz.timezone(tz)
    c_with_timestamp = []
    for c in clockings:
        timestamp = datetime.fromtimestamp(int(c[0]), tz=tzinfo).strftime('%H:%M:%S %A %d-%b-%y')
        card = c[1]
        person_name = get_two_lines_name(card).replace("\n"," ")
        c_with_timestamp.append((timestamp, card, person_name))


    return render_template('show_stored_clockings.html', clockings=c_with_timestamp)

