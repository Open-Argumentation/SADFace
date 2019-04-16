#!/usr/bin/python

import configparser as cp

current = cp.ConfigParser()
config_location = "etc/defaults.cfg"

def load():
    """
    """
    try:
        current.read(config_location)
    except:
        print("Could not read configs from "+ config_location)
        exit(1) 

def set_config_location(location):
    """
    Enable the location of custom configuration files to be supplied
    """
    global config_location
    config_location = location


