from flask import Flask

#from flask_security import Security
#from flask_cors import CORS
import models
from views import register_blueprint
from lib import config



def create_app():
    app = Flask(__name__)
    app.jinja_env.auto_reload = True
    app.config.from_object(config.Config())
    #CORS(app)
    
    # models setup
    models.setup(app)

    # security setup

    #Security(app, models.user.USER_DATASTORE,login_form=models.user.ExtendedLoginForm)

    # register app
    register_blueprint(app)
    return app






if __name__ == "__main__":

    app = create_app()
    #app.run("192.168.127.77",port=55001)
    app.run("0.0.0.0", port=8001)
#"192.168.111.128",port=55001