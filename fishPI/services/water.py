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
    services.database.set_initial("co2_state", "off")
    services.database.set_initial("co2_on_hour", "10")
    services.database.set_initial("co2_off_hour", "20")

    fishPI.services.water.tick_count = int(services.database.get_meta("tick_count").value)

    if(hasGPIO):    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(fishPI.config.flow_pin), GPIO.IN)
        services.water.set_solenoid_off()
        GPIO.add_event_detect(int(fishPI.config.flow_pin), GPIO.BOTH, callback=services.water.tick_pulse)

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

#Get the WC Schedule
def get_water_schedule():
    return fishPI.services.database.get_meta("water_schedule")

#Set the WC Schedule
def set_water_schedule(schedule):
    return fishPI.services.database.set_meta("water_schedule", schedule)

#Get the WC Flow Pulse Count
def get_water_ticks():
    return fishPI.services.database.get_meta("tick_count")

#Calculate and update ticks this hour
def update_water_hour():

    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = str(int(str(time.strftime("%H"))))
    log[hour] = int(fishPI.services.water.tick_count)

    fishPI.services.database.set_meta("water_log", json.dumps(log))
    return ticks_to_litres(log[hour])

#Get the litres this hour
def get_water_hour():

    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = str(int(str(time.strftime("%H"))))
    last_hour = str(int(str( (datetime.datetime.now() + datetime.timedelta(hours = -1)).strftime("%H") )))
    ticks_this_hour = int(log[hour]) - int(log[last_hour])

    return float(ticks_to_litres(ticks_this_hour))

#Get the litres this day
def get_water_day():

    log = json.loads(fishPI.services.database.get_meta("water_log").value)
    hour = str(int(str(time.strftime("%H"))))
    midnight = "0"
    return float(ticks_to_litres(log[hour])) - float(ticks_to_litres(log[midnight]))

def ticks_to_litres(ticks):
    return (float(ticks) * 0.0025)

def litres_to_ticks(litres):
    return (float(litres) / 0.0025)

#Get the litres total
def get_water_total():
    return float(ticks_to_litres(fishPI.services.database.get_meta("tick_count").value))

#Count a pulse if the input state has changed
def tick_pulse(caller):
    print("called...")
    if GPIO.input(int(fishPI.config.flow_pin)) != fishPI.services.water.pin_state:
        fishPI.services.water.pin_state = GPIO.input(int(fishPI.config.flow_pin))
        fishPI.services.water.tick_count = int(fishPI.services.water.tick_count) + 1
        fishPI.services.database.set_meta("tick_count", fishPI.services.water.tick_count)
        fishPI.services.water.update_water_hour()

#Get the WC Log
def get_log():
    return fishPI.services.database.get_meta("water_log")

#Get Remaining litres for this hour
def get_water_remaining_this_hour():
    
    hour = str(int(str(time.strftime("%H"))))
    schedule = json.loads(fishPI.services.water.get_water_schedule().value)

    changed_this_hour = fishPI.services.water.get_water_hour()
    to_change_this_hour = schedule[hour]

    remaining = float(to_change_this_hour) - float(changed_this_hour)
  
    if(remaining < 0):
        return 0
    else:
        return float(remaining)

def get_water_remaining_this_day():

    schedule = json.loads(fishPI.services.water.get_water_schedule().value)
    water_changed_today = get_water_day()

    total = 0

    for hour in schedule:
        total = float(total) + float(schedule[hour])

    remaining = total - water_changed_today

    if(remaining < 0):
        return 0
    else:
        return remaining

#Do the WC Scheduler
def do_water_schedule():

    if(get_solenoid_status() == "on"):
        return 0

    wc_this_hour = fishPI.services.water.get_water_remaining_this_hour()

    if(wc_this_hour > 0): #Water Change is due

        ticks_now = get_water_ticks().value
        ticks_finish = int(ticks_now) + int(litres_to_ticks(wc_this_hour))

        logging.logInfo("Changing Water {} from {} ticks to {} ticks".format(str(wc_this_hour), str(get_water_ticks().value), str(ticks_finish)))

        while( int(get_water_ticks().value) < ticks_finish ):
            fishPI.services.water.set_solenoid_on()
            
        fishPI.services.water.set_solenoid_off()
            
    else:

        fishPI.services.water.set_solenoid_off()
        return 0