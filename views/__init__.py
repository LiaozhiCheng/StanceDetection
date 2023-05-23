from .sentiment_api import sentiment_api
#from .summarization_api import summarization_api
from .stance_api import stance_api
project_code = "5000"
global_prefix = "/cdal/" + project_code + "/api"
blueprint_prefix = [(sentiment_api, '/sentiment/'),(stance_api, '/stance/')]
version = "v1"
def register_blueprint(app):
    for blueprint, prefix in blueprint_prefix:
        app.register_blueprint(blueprint, url_prefix=global_prefix + prefix + version)
    return app