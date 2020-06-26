#!/usr/bin/python

from configparser import ConfigParser
import os

current = None
location = None 

def generate():
    """
    Convenience function to create a default SADFace configuration file if one is needed
    """
    config = ConfigParser()
    
    if not os.path.exists('new.cfg'):
        config['analyst'] = {'name': 'A User', 'email': 'user@email.address'}
        config['file'] = {'name': 'data', 'dir': 'deploy/out/'}
        config['db'] = {'name':'argdb', 'type':'couchdb', 'ip':'127.0.0.1', 'port':'5984', 'protocol':'http'}
    
    config.write(open('new.cfg', 'w'))


def init(location=None):
    """
    Function to initialise the SADFace configuration
    """
    if(location is not None):
        set_location(location)
        load()
    else:
        reset()


def load():
    """
    Load a configuration file from the stored config_location
    """
    if(location is not None):
        try:
            global current
            current = ConfigParser()
            current.read(location)
        except:
            print("Could not read configs from " + location)
            exit(1) 
    else:
        raise Exception("Tried to load config file but location is set to None")
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


