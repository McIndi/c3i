import os
import sys
import util
import json
import atexit
import readline
import argparse
import cherrypy
import platform
from time import time
from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
from cherrypy.wsgiserver import CherryPyWSGIServer

if "Windows" in platform.system():
	home = "C:\\Program Files"
	c3i_home = os.path.join(home, "c3i")
	c3i_config = os.path.join(c3i_home, "config.json")
elif "Linux" in platform.system():
	home = os.path.expanduser("~")
	c3i_home = os.path.join(home, ".c3i")
	c3i_config = os.path.join(c3i_home, "config.json")

if not os.path.exists(c3i_home):
    util.first_run()

with open(c3i_config, "r") as fin:
    config = json.load(fin)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    return parser.parse_args(argv)


def main(argv=None):
    plugins = util.plugins()
    for name, plugin in plugins.items():
        cherrypy.tree.graft(plugin(config), "/{}".format(name))

    cherrypy.config.update({
        'engine.autoreload.on': False,
        'log.screen': False,
        'log.access_file': str(config["access.log"]),
        'log.error_file': str(config["error.log"]),
        'server.socket_port': int(config["port"]),
        'server.socket_host': str(config["host"]),
        'server.max_request_body_size': int(config["max_request_body_size"]),
        'engine.SIGHUP': None,
        'engine.SIGTERM': None,
    })

    cherrypy.server.ssl_module = 'builtin'
    CherryPyWSGIServer.ssl_adapter = BuiltinSSLAdapter(
        config["cert"],
        config["key"],
        None)
    print("Serving on https://{}:{}".format(config["host"], config["port"]))
    cherrypy.engine.start()
    cherrypy.engine.block()

    
if __name__ == "__main__":
    main()

