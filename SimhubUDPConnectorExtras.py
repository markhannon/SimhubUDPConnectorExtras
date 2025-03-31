'''SimHubUDPConnectorExtras - Send additional AC information to SimHub'''

#pylint: disable=import-error, unused-argument, unused-import, unused-wildcard-import, wildcard-import

import configparser
import json
import os.path
import platform
import sys

import ac
import acsys

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + "/stdlib64"
else:
    sysdir = os.path.dirname(__file__) + "/stdlib"

sys.path.insert(0, sysdir)
os.environ["PATH"] = os.environ["PATH"] + ";."

import ctypes 
from ctypes import *

from third_party.sim_info import info
from constants import APP_NAME, APP_PATH
from settings import Settings
from tyres import Tyres, TyresError
from udp_data_stream import UDPDataStream

##################################################
# Configuration variables
##################################################

settings = Settings()
settings.read_settings()
simhub = UDPDataStream(settings.ip, settings.port)

##################################################
# Global variables
##################################################

car_name = ''
tyre_new = ""
tyre_old = ""
tyres = None

l_data = ''
l_udp = ''

launch_time = 0

##################################################
# Assetto Corsa functions
##################################################


def acMain(ac_version):

    global car_name, l_data, l_udp

    car_name = ac.getCarName(0)

    # App window
    appWindow = ac.newApp(APP_NAME)
    ac.setTitle(appWindow, APP_NAME)
    ac.setSize(appWindow, 350, 250)
    l_data = ac.addLabel(appWindow, '{}')
    ac.setPosition(l_data, 5, 30)
    l_udp = ac.addLabel(appWindow, simhub.status())
    ac.setPosition(l_udp, 5, 200)
    return APP_NAME


def acUpdate(deltaT):
    global l_data, l_udp, tyre_new, tyre_old, tyres, launch_time

    ac.setText(l_udp, simhub.status())

    launch_time += + deltaT

    tyre_new = info.graphics.tyreCompound
    if launch_time > 3 and tyre_new != tyre_old:
        tyre_old = tyre_new
        try:
            tyres = Tyres(car_name, tyre_new)
            ac.setText(l_data, json.dumps(
                tyres.data(), indent=4, sort_keys=True))
            simhub.send(tyres.data())
        except TyresError as err:
            ac.log(err)
            ac.console(err)


# Do on AC shutdown
def acShutdown():
    simhub.close()
