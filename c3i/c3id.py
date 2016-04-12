import os
import c3i
import sys
import util
import logging
import platform
import cherrypy
import pkg_resources
from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
from cherrypy.wsgiserver import CherryPyWSGIServer

home = os.path.expanduser("~")
c3i_home = os.path.join(home, ".c3i")
log_dir = os.path.join(c3i_home, "log")

logging.basicConfig(filename=os.path.join(log_dir, "c3id.log"),
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # Windows
    import win32serviceutil
    import servicemanager
    import win32service
    import win32event
    import socket
except ImportError:
    # Posix
    from daemon import Daemon
    from time import sleep

def run(config):
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
    cherrypy.engine.start()
    cherrypy.engine.block()

    
if "Windows" in platform.system():
    class C3Id(win32serviceutil.ServiceFramework):
        """
        A class representing C3Id on windows
        """
        _svc_name_ = "c3id"
        _svc_display_name_ = "c3id"

        def SvcStop(self):
            """
            Stop the service.
            """

            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            cherrypy.engine.exit()
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

        def SvcDoRun(self):
            """
            Start the service.
            """
            servicemanager.LogInfoMsg("Starting c3id")
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            servicemanager.LogInfoMsg("Entering Main method")
            try:
                run(c3i.config)
            except:
                logger.exception("An unhandled exception occurred")
                raise
        
elif "Linux" in platform.system():
    class C3Id(Daemon):
        """
        A class representing C3Id on a posix system
        """
        def run(self):
            """
            main method, this does most of the work
            """
            logger.debug("starting main")
            try:
                run(c3i.config)
            except:
                logger.exception("An unhandled exception occurred")
                raise
            logger.debug("main returned")

        def status():
            raise NotImplementedError
