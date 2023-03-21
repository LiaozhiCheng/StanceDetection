from flask import Flask




def create_app():
    app = Flask(__name__)
    app.jinja_env.auto_reload = True
    #app.config.from_object(config.Config())
    @app.route("/")
    def index():
        return "hello"
    return app






if __name__ == "__main__":

    app = create_app()
    app.run("192.168.127.77",port=55001)
    
#"192.168.111.128",port=55001