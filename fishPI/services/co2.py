import fishPI
import os.path
import json
import time
import datetime
from dateutil import parser

from fishPI import logging
from fishPI import services
from fishPI import models
from fishPI import config

try:
    import RPi.GPIO as GPIO
    hasGPIO = True
except ImportError:
    hasGPIO = False

pin_state = ""
tick_count = 0

def load():
    services.database.set_initial("co2_state", "off")
    services.database.set_initial("co2_on_hour", "10")
    services.database.set_initial("co2_off_hour", "20")

    if(hasGPIO):    
        GPIO.setmode(GPIO.BCM)
        services.co2.set_co2_off

#Get CO2 PIN State
def get_co2_status():
    return services.database.get_meta("co2_state").value

#Switch off the CO2 PIN
def set_co2_off():
    if(hasGPIO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(int(fishPI.config.co2_pin),GPIO.OUT)
        GPIO.output(int(fishPI.config.co2_pin),GPIO.HIGH)

    services.database.set_meta("co2_state","off")

#Switch on the CO2 PIN
def set_co2_on():
    if(hasGPIO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(int(fishPI.config.co2_pin),GPIO.OUT)
        GPIO.output(int(fishPI.config.co2_pin),GPIO.LOW)
        
    services.database.set_meta("co2_state","on")

def get_co2_off_hour():
    return services.database.get_meta("co2_off_hour")

def get_co2_on_hour():
    return services.database.get_meta("co2_on_hour")

def set_co2_off_hour(hour):
    services.database.set_meta("co2_off_hour",hour)

def set_co2_on_hour(hour):
    services.database.set_meta("co2_on_hour",hour)

def do_co2_schedule():
    hour = str(int(str(time.strftime("%H"))))

    on = get_co2_on_hour().value
    off = get_co2_off_hour().value

    if(int(hour) >= int(on) and int(hour) < int(off)):
        set_co2_on()

    if(int(hour) >= int(off)):
        set_co2_off()

    if(int(hour) < int(on)):
        set_co2_off()
