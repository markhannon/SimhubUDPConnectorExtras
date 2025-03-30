'''SimHubUDPConnectorExtras - Send additional AC information to SimHub'''

import ac
import acsys
import sys
import os.path
import platform
import json


if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + "/stdlib64"
else:
    sysdir = os.path.dirname(__file__) + "/stdlib"

sys.path.insert(0, sysdir)
os.environ["PATH"] = os.environ["PATH"] + ";."

import ctypes
from ctypes import *
from third_party.sim_info import info

from Tyres import Tyres, TyresError
from UDPDataStream import UDPDataStream 

##################################################
# Configuration variables
##################################################
APP_NAME = 'SimHubUDPConnectorExtras'
UDP_IP = "127.0.0.1"
UDP_PORT = 20777

##################################################
# Global variables
##################################################
car = ''
tyre_new = ""
tyre_old = ""
tyres = None
udp_data_stream = None

l_data = ''
launchTime = 0

##################################################
# Assetto Corsa functions
##################################################

def acMain(ac_version):
    
    global car, l_data, udp_data_stream
    
    car = ac.getCarName(0)
    udp_data_stream = UDPDataStream(UDP_IP, UDP_PORT)

    # App window
    appWindow = ac.newApp(APP_NAME)
    ac.setTitle(appWindow, APP_NAME)
    ac.setSize(appWindow, 400,200)
    l_data = ac.addLabel(appWindow, '{}')
    ac.setPosition(l_data, 5, 30)
    return APP_NAME 

def acUpdate(deltaT):
    
    global l_data, tyre_new, tyre_old, tyres, launchTime
    launchTime = launchTime + deltaT 
    
    tyre_new = info.graphics.tyreCompound

    if launchTime  > 3 or tyre_new != tyre_old:
        tyre_old = tyre_new
        try:
            tyres = Tyres(car, tyre_new)
            ac.setText(l_data, json.dumps(tyres.data(), indent=4, sort_keys=True))
            udp_data_stream.send(tyres.data())
        except TyresError as err:
            ac.log(err)  # Print error to console and log file
            ac.console(err) 


# Do on AC shutdown
def acShutdown():
    udp_data_stream.close()
