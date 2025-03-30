'''Helper class to read, parse and send Tyre data.'''

import configparser
import re

import ac

class Tyres:
    '''Tyres info class.'''

    def __init__(self, car, tyre):

        self.car = car
        self.idealPressureFront = 0
        self.idealPressureRear = 0
        self.minimumOptimalTemperature = 0
        self.maximumOptimalTemperature = 0
        self.tyre = tyre
        self.tyreCompound = ''

        self.parse_compounds()

    def data(self):
        '''Return data to send to UDPDataSteam.'''
        
        return {
            'idealPressureFront': self.idealPressureFront,
            'idealPressureRear': self.idealPressureRear,
            'minimumOptimalTemperature': self.minimumOptimalTemperature,
            'maximumOptimalTemperature': self.maximumOptimalTemperature,
            'tyreCompound': self.tyre[self.tyre.find("(")+1:self.tyre.find(")")]
            }

    def parse_compounds(self):
        '''Parse the Sidekick compounds database for tyre data.'''

        COMPOUNDS_PATH = "apps/python/Sidekick/compounds/"
    
        basic_ini = configparser.ConfigParser()
        extra_ini = configparser.ConfigParser()
        basic_ini.read(COMPOUNDS_PATH + "compounds.ini")
        extra_ini.read(COMPOUNDS_PATH + self.car + ".ini")
        tyres_idx = re.sub('\_+$', '', re.sub(r'[^\w]+', '_', self.tyre)).lower()
        
        if basic_ini.has_section(self.car + "_" + tyres_idx):
            try:
                self.idealPressureFront = int(basic_ini.get(self.car + "_" + tyres_idx, "IDEAL_PRESSURE_F"))
                self.idealPressureRear = int(basic_ini.get(self.car + "_" + tyres_idx, "IDEAL_PRESSURE_R"))
                self.minimumOptimalTemperature = int(basic_ini.get(self.car + "_" + tyres_idx, "MIN_OPTIMAL_TEMP"))
                self.maximumOptimalTemperature = int(basic_ini.get(self.car + "_" + tyres_idx, "MAX_OPTIMAL_TEMP"))
            except configparser.Error:
                ac.console("Tyres: Error loading tyre data from %s", COMPOUNDS_PATH + "compounds.ini")
        elif extra_ini.has_section(self.car + "_" + tyres_idx):
            try:
                self.idealPressureFront = int(extra_ini.get(self.car + "_" + tyres_idx, "IDEAL_PRESSURE_F"))
                self.idealPressureRear = int(extra_ini.get(self.car + "_" + tyres_idx, "IDEAL_PRESSURE_R"))
                self.minimumOptimalTemperature = int(float(extra_ini.get(self.car + "_" + tyres_idx, "MIN_OPTIMAL_TEMP")))
                self.maximumOptimalTemperature = int(float(extra_ini.get(self.car + "_" + tyres_idx, "MAX_OPTIMAL_TEMP")))
            except configparser.Error:
                ac.console("Tyres: Error loading tyre data from %s", COMPOUNDS_PATH + self.car + ".ini")
        else:
            ac.console("Tyres: Error loading tyre data from compounds.ini and %s.ini", self.car)
