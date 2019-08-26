import fishPI
import os.path
import subprocess
import time, datetime, json

from datetime import datetime  
from datetime import timedelta  

from fishPI import logging
from fishPI import services
from fishPI import models
from fishPI import config

def load():
    services.database.set_initial("lighting_override",0)
    services.database.set_initial("ambients_type","none")
    services.database.set_initial("ambients_duration",0)
    return true

def set_lighting_override():
        services.database.set_meta("lighting_override",str(percentage))

def set_ambients_cloudy(duration = 10):
    set_lighting_override("cloudy", duration)

def set_ambients_stormy(duration = 10):
    set_lighting_override("stormy", duration)

def set_ambients_rainy(duration = 10):
    set_lighting_override("rainy", duration)

def set_ambients_nature(duration = 10):
    set_lighting_override("nature", duration)

def set_ambients(ambient, duration = 0):
    services.database.set_meta("ambients_type",ambient)
    services.database.set_meta("ambients_duration",duration)

def clear_ambients():

    set = services.database.get_meta("ambients_duration")
    if(set.value > 0):

        clear_time = set.added + timedelta(minutes=int(set.value))  

        if(clear_time > datetime.now()):
            set_ambients("none",0) 