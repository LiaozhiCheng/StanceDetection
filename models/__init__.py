
def setup(app):
    # import those packages that need db
    from . import _model
    _model.setup()

