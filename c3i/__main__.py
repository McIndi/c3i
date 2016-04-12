import os
import sys
import platform

home = os.path.expanduser("~")
c3i_home = os.path.join(home, ".c3i")

if "Windows" in platform.system():
    import win32serviceutil

    def main():
        from c3id import C3Id

        win32serviceutil.HandleCommandLine(C3Id)

elif "Linux" in platform.system():

    def main():
        from c3id import C3Id

        pid_file = os.path.join(
            c3i_home,
            "c3i.pid")
        c3id = C3Id(pid_file)

        if len(sys.argv) != 2:
            print "USAGE: c3id { start | stop | restart | status }"
            sys.exit(1)

        if "start" in sys.argv[1]:
            c3id.start()
        elif "stop" in sys.argv[1]:
            c3id.stop()
        elif "restart" in sys.argv[1]:
            c3id.restart()
        elif "status" in sys.argv[1]:
            print c3id.status()
        else:
            print "USAGE: c3id { start | stop | restart | status }"
            sys.exit(1)

        sys.exit(0)

if __name__ == "__main__":
    print("entering main")
    main()
    print("Exiting")

