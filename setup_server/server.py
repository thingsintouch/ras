import os
from flask import Flask,send_from_directory
from flask_login import LoginManager
from common.common import get_hashed_machine_id

app = Flask(__name__)

app.config['SECRET_KEY'] = get_hashed_machine_id()
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["FLASK_ENV"] = "development"

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"


###########################
#### BLUEPRINT CONFIGS #######
#########################

# Import these at the top if you want
# We've imported them here for easy reference
from setup_server.core.views import core
from setup_server.ras_info.views import ras_info
from setup_server.commands.views import commands
from setup_server.parameters.views import parameters
from setup_server.factory.views import factory
from setup_server.daily_reboot.views import daily_reboot
from setup_server.wifi_setup.views import wifi_setup
from setup_server.odoo_setup.views import odoo_setup
from setup_server.wifi_delete.views import wifi_delete
from setup_server.users.views import users
from setup_server.error_pages.handlers import error_pages


# Register the apps
app.register_blueprint(wifi_delete)
app.register_blueprint(wifi_setup)
app.register_blueprint(odoo_setup)
app.register_blueprint(ras_info)
app.register_blueprint(commands)
app.register_blueprint(parameters)
app.register_blueprint(daily_reboot)
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(factory)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'faviconThings.ico',mimetype='image/vnd.microsoft.icon')

def server_stop():
    app.stop()

def server():
    app.run(host='0.0.0.0', port=80)

def main():
    server()

if __name__ == '__main__':
    main()