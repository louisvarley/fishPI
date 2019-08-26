import fishPI
import os.path
import json
import time

from fishPI import logging
from fishPI import services
from fishPI import models
from fishPI import config

from fishPI.services import database

# Conditional Try to Import, this only works on PI */
try:
    from w1thermsensor import W1ThermSensor
    hasW1 = True
except:
    hasW1 = False

def load():
    log = {}
 
    for i in range(24):       
        log[i] = 0
    services.database.set_initial("temperature_log",json.dumps(log))
    


def get_temperature():

    if(hasW1):

        try:
  
            sensor = W1ThermSensor()
            temperature = round(sensor.get_temperature(),1)

            min = fishPI.config.load_from_config("temperature_warning","aquarium_min")
            max = fishPI.config.load_from_config("temperature_warning","aquarium_max")

            label = "normal"
            if(temperature > float(max)): label = "over"
            if(temperature < float(min)): label = "under"

        except:
            label = "error"
            temperature = "-"

    else:

        label = "error"
        temperature = "-"

    return {"label": label, "temperature": temperature}

def log_temperature():

    log = get_temperature_log()
    hour = str(int(str(time.strftime("%H"))))
    temperature = get_temperature()
    log[hour] = temperature['temperature']

    fishPI.services.database.set_meta("temperature_log", json.dumps(log))
    return temperature

def get_temperature_log():
    return json.loads(fishPI.services.database.get_meta("temperature_log").value)

