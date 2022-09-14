from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from setup_server.models import User
from setup_server.users.forms import LoginForm
from setup_server.server import login_manager

from common.constants import PARAMS
from common.params import Params

params = Params(db=PARAMS)

users = Blueprint('users', __name__)

setup_password = params.get("setup_password")

user = User(setup_password, "1") # password and id

# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return user

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        setup_password = params.get("setup_password")
        if form.password.data == setup_password:
            #Log in the user
            
            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form, current_user=current_user)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))



