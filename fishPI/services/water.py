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

flow_state = ""
flow_count = 0

def load():
    services.database.set_initial("solenoid_state","off")
    services.database.set_initial("water_schedule",models.water.schedule().as_json())
    services.database.set_initial("flow_count","0")
    services.database.set_initial("flow_state","off")
    services.database.set_initial("water_log",models.water.schedule().as_json())
    flow_count = services.database.get_meta("flow_count").value

    if(hasGPIO):    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(fishPI.config.flow_pin), GPIO.IN)
        services.water.set_solenoid_off()
        GPIO.add_event_detect(int(fishPI.config.flow_pin), GPIO.BOTH, callback=services.water.count_pulse)

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
    return json.loads(fishPI.services.database.get_meta("water_schedule").value)

def set_schedule(schedule):
    return fishPI.services.database.set_meta("water_schedule", schedule)

def get_flow_count():
    return fishPI.services.database.get_meta("flow_count")

def update_hour_litres():
    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = time.strftime("%H")
    log[hour] = get_litres_total()
    fishPI.services.database.set_meta("water_log", json.dumps(log))
    return log[hour]

def get_hour_litres():
    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = time.strftime("%H")
    lastHour = str(int(str( (datetime.datetime.now() + datetime.timedelta(hours = -1)).strftime("%H") )))

    return log[hour] - log[lastHour] 


def get_day_litres():

    hour = time.strftime("%H")
    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    total = 0

    for i in range(int(hour)):
        total = float(total) + float(log[str(i)])
    
    return total

def get_litres_total():
    return float(fishPI.services.database.get_meta("flow_count").value) * (0.8489164086687307)/1000

def count_pulse(caller):
	if GPIO.input(int(fishPI.config.flow_pin)) != fishPI.services.water.flow_state:
		fishPI.services.water.flow_state = GPIO.input(int(fishPI.config.flow_pin))
		fishPI.services.water.flow_count = fishPI.services.water.flow_count + 1
		fishPI.services.database.set_meta("flow_count", fishPI.services.water.flow_count)

def get_log():
    return fishPI.services.database.get_meta("water_log").value

def left_to_change_this_hour():
    
    hour = time.strftime("%H")
    schedule = fishPI.services.water.get_schedule()
    changedThisHour = fishPI.services.water.get_hour_litres()
    toChangeThisHour = schedule[hour]
    remaining = float(toChangeThisHour) - float(changedThisHour)

    if(remaining < 0):
        return 0
    else:
        return remaining

def do_schedule():

    if(fishPI.services.water.left_to_change_this_hour() > 0):

        fishPI.services.water.set_solenoid_on()

        services.database.set_meta("flow_state","on")

        while(fishPI.services.water.left_to_change_this_hour > 0):
            started = datetime.strptime(services.database.get_meta("flow_state").added)
            now = datetime.datetime.now()
            if( (now - started).total_seconds() > 60 ):
                logging.logWarning("Safety Stopped water change for taking over 60 seconds")
                fishPI.services.water.set_solenoid_off()

        fishPI.services.water.set_solenoid_off()

    else:
        fishPI.services.water.set_solenoid_off()
        return False