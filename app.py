# Welcome to the Flask-Bootstrap sample application. This will give you a
# guided tour around creating an application using Flask-Bootstrap.
#
# To run this application yourself, please install its requirements first:
#
#   $ pip install -r sample_app/requirements.txt
#
# Then, you can actually run the application.
#
#   $ flask --app=sample_app dev
#
# Afterwards, point your browser to http://localhost:5000, then check out the
# source.
#
from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_debug import Debug
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .frontend import frontend
from .nav import nav
from .default_config import SECRET_KEY
from .api import LightTracker

# We are using the "Application Factory"-pattern here, which is described
# in detail inside the Flask docs:
# http://flask.pocoo.org/docs/patterns/appfactories/

app = Flask(__name__)

CSRFProtect(app)
Debug(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'

# We use Flask-Appconfig here, but this is not a requirement
AppConfig(app)

# Install our Bootstrap extension
Bootstrap(app)

# Our application uses blueprints as well; these go well with the
# application factory. We already imported the blueprint, now we just need
# to register it:
app.register_blueprint(frontend)

# Because we're security-conscious developers, we also hard-code disabling
# the CDN support (this might become a default in later versions):
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'devkey'

# We initialize the navigation as well

nav.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
