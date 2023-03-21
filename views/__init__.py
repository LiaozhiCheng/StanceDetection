from .sentiment_api import sentiment_api
#from .summarization_api import summarization_api
from .stance_api import stance_api

blueprint_prefix = [(sentiment_api, ''),(stance_api, '')]

def register_blueprint(app):
    for blueprint, prefix in blueprint_prefix:
        app.register_blueprint(blueprint, url_prefix=prefix)
    return app