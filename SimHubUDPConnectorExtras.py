'''SimHubUDPConnectorExtras - Send additional AC information to SimHub'''

import platform
import os
import sys

import ac
import acsys

from third_party.sim_info import info

from Tyres import Tyres
from UDPDataStream import UDPDataStream

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + "/stdlib64"
else:
    sysdir = os.path.dirname(__file__) + "/stdlib"

sys.path.insert(0, sysdir)
os.environ["PATH"] = os.environ["PATH"] + ";."

##################################################
# Configuration variables
##################################################
APP_NAME = 'SimHubUDPConnectorExtras'
UDP_IP = "127.0.0.1"
UDP_PORT = 30777

##################################################
# Global variables
##################################################
car = ''
tyre_new = ''
tyre_old = ''
tyres = None
udp_data_stream = None

##################################################
# Assetto Corsa functions
##################################################

def acMain(ac_version):
    
    global car, udp_data_stream
    
    car = ac.getCarName(0)
    udp_data_stream = UDPDataStream(UDP_IP, UDP_PORT, debug=True)

    ac.log("Hello: %s", APP_NAME)
    ac.console("Hello: %s", APP_NAME)

    # App window
    appWindow = ac.newApp(APP_NAME)
    ac.setTitle(appWindow, "")
    ac.drawBorder(appWindow, 0)


def acUpdate(deltaT):
    
    global tyre_new, tyre_old, tyres

    tyre_new = info.graphics.tyreCompound
    ac.log("%s", tyre_new)
    if tyre_new != tyre_old:
        ac.console("%s: Changed from %s to %s tyres", tyre_old, tyre_new)
        tyre_old = tyre_new
        tyres = Tyres(car, tyre_new)
        udp_data_stream.send(tyres.data())

    



# Do on AC shutdown
def acShutdown():
    udp_data_stream.close()
