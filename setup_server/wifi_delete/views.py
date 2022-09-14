from flask import render_template,url_for,flash, redirect,request,Blueprint, jsonify
from flask_login import current_user,login_required
from setup_server.wifi_delete.forms import WiFiDelete, WiFiDeleteResult, get_existent_connections
from common.common import runShellCommand_and_returnOutput as rs

wifi_delete = Blueprint('wifi_delete',__name__)

@wifi_delete.route('/wifi_delete',methods=['GET','POST'])
@login_required
def delete_wifi():
    form = WiFiDelete()
    if form.validate_on_submit():
        print(form.connection_to_delete.data)
        connection_to_delete = form.connection_to_delete.data
        existent_connections = get_existent_connections()
        if len(existent_connections) > 1:
            answer = (rs("sudo nmcli connection delete " + connection_to_delete))
            if "successfully deleted" in answer:
                result = 1
            else:
                result = 0
        else:
            result = 2
        return redirect(url_for('wifi_delete.wifi_delete_result', result=result ))
    return render_template('wifi_delete.html', form=form)

@wifi_delete.route('/wifi_delete/<int:result>',methods=['GET','POST'])
@login_required
def wifi_delete_result(result):
    form=WiFiDeleteResult()
    if result == 1:
        result_for_html = "Deleted successfully."
    elif result ==2:
        result_for_html = "Will not delete the last WiFi connection (this is a design choice)."
    else:
        result_for_html = "Failed. Could not delete WiFi connection."

    if form.validate_on_submit():
        return redirect(url_for('core.index'))

    return render_template('wifi_delete_result.html', result=result_for_html, form=form)

@wifi_delete.route('/connections')
@login_required
def existing_connections():
    existent_connections = get_existent_connections()

    connectionsArray = []

    for conn in existent_connections:
        connObj = {}
        connObj['id'] = conn[0]
        connObj['name'] = conn[1]
        connectionsArray.append(connObj)

    return jsonify({'connections' : connectionsArray})