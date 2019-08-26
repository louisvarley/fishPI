import fishPI
import os.path
import subprocess
import time, datetime, json

from fishPI import logging
from fishPI import services
from fishPI import models
from fishPI import config

from fishPI.services import database

def load():
    for i, pin in enumerate(fishPI.config.light_pins):
        channel = i+1
        services.database.set_initial("{}_brightness".format(channel),0)
        services.database.set_initial("{}_schedule".format(channel),models.lighting.schedule().as_json())

def light_channel_meta(channel):
    return "{}_brightness".format(channel)

def schedule_channel_meta(channel):
    return "{}_schedule".format(channel)
                         
def channel_to_pin(channel):
    return int(fishPI.config.load_from_config("light_pins",channel))

def get_schedule(channel):
    return fishPI.services.database.get_meta(schedule_channel_meta(channel))

def set_schedule(channel, schedule):
    return fishPI.services.database.set_meta(schedule_channel_meta(channel), schedule)

def get_brightness(channel):
    return fishPI.services.database.get_meta(light_channel_meta(channel))

def set_brightness(channel, percentage):
    brightness_now = get_brightness(channel)
    current_percentage = int(brightness_now.value)
    percentage = int(percentage)

    override = fishPI.services.database.get_meta("lighting_override").value

    if(int(override) > 0): percentage = override

    pi_blaster(channel_to_pin(channel), percentage)

    return fishPI.services.database.set_meta(light_channel_meta(channel),str(percentage))

def flash(channel):
        pi_blaster(channel_to_pin(channel), 0)
        pi_blaster(channel_to_pin(channel), 100)
        pi_blaster(channel_to_pin(channel), 0)
        pi_blaster(channel_to_pin(channel), get_brightness(channel).value)

def pi_blaster(pin,percentage):

    if(isinstance(percentage, str)):
        percentage = float(percentage)

    if(percentage > 100):
        percentage = 100

    if(percentage < 0):
        percentage = 0

    v = (percentage / 100)

    if(os.path.exists('/dev/pi-blaster')):
        subprocess.Popen('echo "{}={}" > /dev/pi-blaster'.format(pin,v), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        print('echo "{}={}" > /dev/pi-blaster'.format(pin,v))

def set_brightness_all(percentage):

    percentage = int(percentage)
    for i, pin in enumerate(fishPI.config.light_pins):
        channel = i+1
        set_brightness(channel,percentage)

def get_brightness_average():

    total = 0
    for i, pin in enumerate(fishPI.config.light_pins):
        channel = i+1
        
        total = total + int(get_brightness(channel).value)

    return round((total / i),0)


def get_brightness_all():

    results = {}
    for i, pin in enumerate(fishPI.config.light_pins):  
        channel = i+1
        results[channel] = (get_brightness(channel).value)

    return results

def do_schedule():

    thisHour = str(int(str(time.strftime("%H"))))
    thisMinute = str(int(str(time.strftime("%M"))))
    nextHour = str(int(str( (datetime.datetime.now() + datetime.timedelta(hours = 1)).strftime("%H") )))
    
    for i, pin in enumerate(fishPI.config.light_pins):
        channel = i+1

        schedule =  json.loads(get_schedule(channel).value)

        brightnessThisHour = int(schedule[thisHour])
        brightnessNextHour = int(schedule[nextHour])

        difference = 0 - (brightnessThisHour - brightnessNextHour)
        differencePerMinute = difference / 60
        differenceThisMinute = round(differencePerMinute * int(thisMinute),1)
        newBrightness = brightnessThisHour + differenceThisMinute

        set_brightness(channel,newBrightness)






