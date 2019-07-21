import fishPI
import os.path
from fishPI import logging
from fishPI import services
from fishPI import models

def load():
    channel = 0
    while channel < len(fishPI.config.light_pins) :
        channel = channel + 1
        services.database.set_initial("{}_brightness".format(channel),0)
        services.database.set_initial("{}_schedule".format(channel),models.lighting.schedule().as_json())

def light_channel_meta(channel):
    return "{}_brightness".format(channel)

def schedule_channel_meta(channel):
    return "{}_schedule".format(channel)
                         
def channel_to_pin(channel):
    return fishPI.config.light_pins[int(channel)]

def get_schedule(channel):
    return fishPI.services.database.get_meta(schedule_channel_meta(channel))

def set_schedule(channel, schedule):
    return fishPI.services.database.set_meta(schedule_channel_meta(channel), schedule)

def get_brightness(channel):
    return fishPI.services.database.get_meta(light_channel_meta(channel))

def set_brightness(channel, percentage):
    current_percentage = float(get_brightness(channel).value)
    percentage = float(percentage)

    if(percentage == current_percentage): get_brightness(channel) 

    if(current_percentage < percentage):
        change_per_increment = int(current_percentage) + int(percentage) / 30
    else:
        change_per_increment = int(current_percentage) - int(percentage) / 30

    x = 0
    while x <= 30:
        x = x + 1
        pi_blaster(channel_to_pin(channel), current_percentage + (change_per_increment * x))

    return fishPI.services.database.set_meta(light_channel_meta(channel),str(percentage))
    

def flash_channel(channel):
        pi_blaster(channel_to_pin(channel), 0)
        pi_blaster(channel_to_pin(channel), 100)
        pi_blaster(channel_to_pin(channel), 0)

def pi_blaster(pin,percentage):

    if(percentage > 100):
        percentage = 100

    if(percentage < 0):
        percentage = 0

    v = round((percentage / 100),1)
   
    if(os.path.exists('/dev/pi-blaster')):
        with open('/dev/pi-blaster', 'w') as printer:
            printer.write("{} = {}".format(pin,v))
    else:
        print("Blasting Pin {} with {}".format(pin,v))