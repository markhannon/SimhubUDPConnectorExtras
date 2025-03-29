import ac, acsys
import platform, os, sys
import codecs, json

UDP_IP = "127.0.0.1"
UDP_PORT = 30777

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + "/stdlib64"
else:
    sysdir = os.path.dirname(__file__) + "/stdlib"

sys.path.insert(0, sysdir)
os.environ["PATH"] = os.environ["PATH"] + ";."

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP


def sendUDPDatastream(data):
    sock.sendto(bytes(json.dumps(data), "UTF-8"), (UDP_IP, UDP_PORT))


def acMain(ac_version):
    # App window
    appWindow = ac.newApp("SimHubUDPConnectorExtras")
    ac.setTitle(appWindow, "")
    ac.drawBorder(appWindow, 0)


def acUpdate(deltaT):
    data = {
        "rpm": ac.getCarState(0, acsys.CS.RPM),
        "turbo": ac.getCarState(0, acsys.CS.TurboBoost),
        "kersCharge": ac.getCarState(0, acsys.CS.KersCharge),
        "kersInput": ac.getCarState(0, acsys.CS.KersInput),
        "clutch": ac.getCarState(0, acsys.CS.Clutch),
        "brake": ac.getCarState(0, acsys.CS.Brake),
        "throttle": ac.getCarState(0, acsys.CS.Gas),
        "ffb": ac.getCarState(0, acsys.CS.LastFF),
        "gear": ac.getCarState(0, acsys.CS.Gear),
        "driveTrainSpeed": ac.getCarState(0, acsys.CS.DriveTrainSpeed),
    }
    sendUDPDatastream(data)


# Do on AC shutdown
def acShutdown():
    sock.close()
