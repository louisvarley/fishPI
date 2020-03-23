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
    services.database.set_initial("solenoid_state","off")
    services.database.set_initial("water_schedule",models.water.schedule().as_json())
    services.database.set_initial("tick_count","0")
    services.database.set_initial("water_log",models.water.schedule().as_json())

    fishPI.services.water.tick_count = int(services.database.get_meta("tick_count").value)

    if(hasGPIO):    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(fishPI.config.flow_pin), GPIO.IN)
        services.water.set_solenoid_off()
        GPIO.add_event_detect(int(fishPI.config.flow_pin), GPIO.BOTH, callback=services.water.tick_pulse)

#Switch off the Solenoid PIN
def set_solenoid_off():
    if(hasGPIO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(int(fishPI.config.solenoid_pin),GPIO.OUT)
        GPIO.output(int(fishPI.config.solenoid_pin),GPIO.HIGH)

    services.database.set_meta("solenoid_state","off")

#Switch on the Solenoid PIN
def set_solenoid_on():
    if(hasGPIO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(int(fishPI.config.solenoid_pin),GPIO.OUT)
        GPIO.output(int(fishPI.config.solenoid_pin),GPIO.LOW)
        
    services.database.set_meta("solenoid_state","on")

#Get Solenoid PIN Status
def get_solenoid_status():

    return services.database.get_meta("solenoid_state").value

#Update the Water Log
def update_log():

    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = str(int(str(time.strftime("%H"))))
    log[hour] = int(fishPI.services.water.tick_count)

    fishPI.services.database.set_meta("water_log", json.dumps(log))
    return ticks_to_litres(log[hour])

#Get the WC Log
def get_log():

    return fishPI.services.database.get_meta("water_log")

#Count a pulse if the input state has changed
def tick_pulse(caller):

    if GPIO.input(int(fishPI.config.flow_pin)) != fishPI.services.water.pin_state:
        fishPI.services.water.pin_state = GPIO.input(int(fishPI.config.flow_pin))
        fishPI.services.water.tick_count = int(fishPI.services.water.tick_count) + 1
        fishPI.services.database.set_meta("tick_count", fishPI.services.water.tick_count)
        fishPI.services.water.update_log()



#Get the water schedule in TICKS
def get_water_schedule_ticks():

    return fishPI.services.database.get_meta("water_schedule")

#Get the water change schedule in LITRES
def get_water_schedule_litres():

    originalSchedule = get_water_schedule_ticks()

    schedule = json.loads(originalSchedule.value);

    for hour in schedule:
        schedule[hour] = ticks_to_litres(schedule[hour])

    return fishPI.models.database.meta("schedule",schedule,str(originalSchedule.added));

#Set the water change schedule using LITRES
def set_water_schedule_litres(schedule):
    schedule = json.loads(schedule)

    for hour in schedule:
        schedule[hour] = litres_to_ticks(schedule[hour])

    return fishPI.services.database.set_meta("water_schedule", schedule)

#Get the Total Tick Count
def get_water_total_ticks():

    return fishPI.services.database.get_meta("tick_count")

#Get the Total Litre Count
def get_water_total_litres():

    return int(ticks_to_litres(get_water_total_ticks()))

#Get the LITRES this HOUR
def get_water_total_hour_litres():

    return float(ticks_to_litres(get_water_hour_ticks()))

# Get the TICKS this HOUR
def get_water_total_hour_ticks():
    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = str(int(str(time.strftime("%H"))))
    last_hour = str(int(str( (datetime.datetime.now() + datetime.timedelta(hours = -1)).strftime("%H") )))
    ticks_this_hour = int(log[hour]) - int(log[last_hour])
    
    return int(ticks_this_hour)

#Get the LITRES this day
def get_water_total_day_litres():

    return float(ticks_to_litres(get_water_total_day_ticks()))

#Get the TICKS this day
def get_water_total_day_ticks():

    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = str(int(str(time.strftime("%H"))))
    midnight = "0"
    return (log[hour]) - (log[midnight])

#Get Ticks remaining this hour
def get_water_ticks_remaining_hour():
    hour = str(int(str(time.strftime("%H"))))
    schedule = json.loads(fishPI.services.water.get_water_schedule_ticks().value)

    changed_this_hour = fishPI.services.water.get_water_total_hour_ticks()
    to_change_this_hour = schedule[hour]

    remaining = int(to_change_this_hour) - int(changed_this_hour)
  
    if(remaining < 0):
        return 0
    else:
        return int(remaining)

#Get Litres remaining this hour
def get_water_litres_remaining_hour():
    
    return float(ticks_to_litres(get_water_ticks_remaining_hour()))

#Get Ticks remaining this day
def get_water_ticks_remaining_day():

    schedule = json.loads(fishPI.services.water.get_water_schedule_ticks().value)
    ticks_today = get_water_total_day_ticks()

    total = 0

    for hour in schedule:
        total = int(total) + int(schedule[hour])

    remaining = total - ticks_today

    if(remaining < 0):
        return 0
    else:
        return remaining

def get_water_litres_remaining_day():

    return float(ticks_to_litres(get_water_ticks_remaining_day()))

#How much water ticks is changed per day
def get_water_ticks_per_day():
    schedule = json.loads(fishPI.services.water.get_water_schedule_ticks().value)

    total = 0

    for hour in schedule:
        total = int(total) + int(schedule[hour])

    return total

#How much water litres is changed per day
def get_water_litres_per_day():

    return ticks_to_litres(get_water_ticks_per_day())

#Do the WC Scheduler
def do_water_schedule():

    #If Already running, do nothing
    if(get_solenoid_status() == "on"):
        return 0

    remaining_this_hour = fishPI.services.water.get_water_ticks_remaining_hour()

    if(remaining_this_hour > 0):

        ticks_now = get_water_ticks().value
        ticks_finish = ticks_now + remaining_this_hour

        logging.logInfo("Changing Water {} from {} ticks to {} ticks".format(str(wc_this_hour), str(get_water_ticks().value), str(ticks_finish)))

        while( int(get_water_total_ticks().value) < ticks_finish ):
            fishPI.services.water.set_solenoid_on()
            
        fishPI.services.water.set_solenoid_off()
            
    else:

        fishPI.services.water.set_solenoid_off()
        return 0

#Convert TICKS to LITRES
def ticks_to_litres(ticks):

    return (float(ticks) * 0.0025)

#Convert LITRES to TICKS
def litres_to_ticks(litres):

    return (int(litres) / 0.0025)

