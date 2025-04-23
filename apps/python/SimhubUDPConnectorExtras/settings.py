'''Helper Class for configuration'''

import configparser

import ac

from constants import APP_PATH


class Settings(configparser.ConfigParser):
    '''Wrapper for settings.ini'''

    SECTION = 'UDPConnectorExtras'
    UDP_IP = 'udp_ip'
    UDP_PORT = 'udp_port'

    SETTINGS = APP_PATH + '/settings.ini'
    SETTINGS_DEFAULTS = APP_PATH + '/settings_defaults.ini'


    def read_settings(self):
        self.read([Settings.SETTINGS_DEFAULTS, Settings.SETTINGS])
        

    @property
    def ip(self):
        return self.get(Settings.SECTION, Settings.UDP_IP)

    @property
    def port(self):
        return self.getint(Settings.SECTION, Settings.UDP_PORT)
