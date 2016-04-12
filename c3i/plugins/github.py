import bottle
import requests
import cherrypy

def plugin(config):
    app = bottle.Bottle(__name__)

    @app.route("/")
    def index():
        resp = requests.get("https://github.com")        
        return resp.text

    return app
