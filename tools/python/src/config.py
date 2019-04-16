#!/usr/bin/python

from configparser import ConfigParser

current = None
config_location = "etc/defaults.cfg"

def load():
    """
    Load a configuration file from the stored config_location
    """
    try:
        global current
        current = ConfigParser()
        current.read(config_location)
    except Exception as e:
        print("Could not read configs from "+ config_location)
        print(e)
        exit(1) 

def set_config_location(location):
    """
    Enable the location of custom configuration files to be supplied
    """
    global config_location
    config_location = location


