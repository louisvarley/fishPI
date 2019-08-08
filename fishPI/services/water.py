import fishPI
import os.path
import json
import time
import datetime

from fishPI import logging
from fishPI import services
from fishPI import models
from fishPI import config

try:
    import RPi.GPIO as GPIO
    hasGPIO = True
except ImportError:
    hasGPIO = False

def load():
    services.database.set_initial("solenoid_state","off")
    services.database.set_initial("water_schedule",models.water.schedule().as_json())

def set_solenoid_off():
    if(hasGPIO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(int(fishPI.config.solenoid_pin),GPIO.OUT)
        GPIO.output(int(fishPI.config.solenoid_pin),GPIO.HIGH)

    services.database.set_meta("solenoid_state","off")

def set_solenoid_on():
    if(hasGPIO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(int(fishPI.config.solenoid_pin),GPIO.OUT)
        GPIO.output(int(fishPI.config.solenoid_pin),GPIO.LOW)

    services.database.set_meta("solenoid_state","on")

def get_solenoid_status():
    return services.database.get_meta("solenoid_state").value

def get_schedule():
    return fishPI.services.database.get_meta("water_schedule")

def set_schedule(schedule):
    return fishPI.services.database.set_meta("water_schedule", schedule)
