#!/usr/bin/python

from configparser import ConfigParser

current = None
location = None 

def load():
    """
    Load a configuration file from the stored config_location
    """
    try:
        global current
        current = ConfigParser()
        current.read(location)
    except:
        print("Could not read configs from "+ config_location)
        exit(1) 

def reset():
    """
    Return config parameters to initial settings
    """
    global current
    global location
    current = None
    location = None

def set_location(new_location):
    """
    Enable the location of custom configuration files to be supplied
    """
    global location
    location = new_location


