import os
import sys
import configparser

from fishPI import logging

title = ""
ui_version = 2
port = 5555
swagger = None
working_dir = None
template_dir = None
static_dir = None
version = 0
flask = None
host_name = ""
app = None
database = None
light_pins = None

def load_from_config(section, setting = None):
    config = configparser.ConfigParser()
    config.read(os.path.join(working_dir,"config.ini"))

    if(setting == None):
        return config.options(section)
    else:
        return str(config.get(str(section),str(setting)))
    
def get_version():
    with open(os.path.join(working_dir, '__version__.py')) as f:
        return int(f.readline().replace('version=',''))

def get_full_version():
    return "1.0." + str(get_version())
