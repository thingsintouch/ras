from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup_server.odoo_setup.forms import OdooForm, OdooResult
from common.common import runShellCommand_and_returnOutput as rs
from bluetooth.connect_To_Odoo import main as connect_to_odoo

odoo_setup = Blueprint('odoo_setup',__name__)

@odoo_setup.route('/odoo_link',methods=['GET','POST'])
@login_required
def odoo_link():
    form = OdooForm()
    if form.validate_on_submit():
        odoo_link = form.odoo_link.data
        if connect_to_odoo(odoo_link):
            result = 1
        else:
            result = 0
        return redirect(url_for('odoo_setup.odoo_result', result=result ))
    return render_template('odoo_setup.html', form=form)

@odoo_setup.route('/odoo_result/<int:result>',methods=['GET','POST'])
@login_required
def odoo_result(result):
    form=OdooResult()
    if result == 1:
        result_for_html = "Connected to Odoo successfully."
    else:
        result_for_html = "Failed. Could not connect to Odoo."

    if form.validate_on_submit():
        return redirect(url_for('core.index'))

    return render_template('odoo_result.html', result=result_for_html, form=form)
    