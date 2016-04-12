import bottle

def plugin(config):
    app = bottle.Bottle(__name__)

    @app.route("/")
    def return_config():
        return config

    return app

