import fishPI
import os.path
import random
from fishPI import logging
from fishPI import services
from fishPI import models

# Conditional Try to Import, this only works on PI */
try:
    from w1thermsensor import W1ThermSensor
    hasW1 = True
except ImportError:
    hasW1 = False

def load():
  load = None

def get_temperature():

    if(hasW1):
        sensor = W1ThermSensor()
        return round(sensor.get_temperature(),1)
    else:
        return round(random.uniform(20,25),1)