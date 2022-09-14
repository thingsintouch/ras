from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup_server.daily_reboot.forms import DailyRebootForm, DailyRebootResult
from common.common import runShellCommand_and_returnOutput as rs
from common.params import Params
from common.constants import PARAMS

params = Params(db=PARAMS)

daily_reboot = Blueprint('daily_reboot',__name__)

@daily_reboot.route('/daily_reboot_time',methods=['GET','POST'])
@login_required
def daily_reboot_time():
    hour_saved = params.get("dailyRebootHour")
    min_saved = params.get("dailyRebootMinute")
    update_saved = params.get("automaticUpdate")
    form = DailyRebootForm()
    if form.validate_on_submit():
        hour_reboot = f'{int(form.hour_reboot.data):02d}'
        minute_reboot = f'{int(form.minute_reboot.data):02d}'
        should_update_firmware_too = form.should_update_firmware_too.data
        params.put("dailyRebootHour", hour_reboot)
        params.put("dailyRebootMinute", minute_reboot)
        if should_update_firmware_too:
            params.put("automaticUpdate","1")
            should_update_firmware_too = "1"
        else:
            params.put("automaticUpdate","0")
            should_update_firmware_too = "0"
        return redirect(url_for('daily_reboot.daily_reboot_result',
            hour=hour_reboot, min=minute_reboot, update=should_update_firmware_too))
    return render_template('daily_reboot.html',
            form=form, hour_saved=hour_saved, min_saved=min_saved, update_saved=update_saved)

@daily_reboot.route('/daily_reboot_result/<hour>/<min>/<update>',methods=['GET','POST'])
@login_required
def daily_reboot_result(hour, min, update):
    form=DailyRebootResult()
    if form.validate_on_submit():
        return redirect(url_for('core.index'))

    return render_template(
        'daily_reboot_result.html',
        form=form,
        hour_reboot = hour,
        minute_reboot = min,
        should_update_firmware_too = update)
    