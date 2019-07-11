import fishPI
from fishPI import logging
from fishPI import services

def light_channel_meta(channel):
    return "brightness_channel_{}".format(channel)

def channel_to_pin(channel):
    return fishPI.config.light_pins[channel]

def get_brightness(channel):
    return fishPI.services.database.get_meta(light_channel_meta(channel))["value"]

def set_brightness(channel, percentage):
    current_percentage = get_brightness(channel)

    if(percentage == current_percentage): return True

    change_per_increment = current_percentage - percentage / 30

    x = 0
    while x <= 30:
        x = X + 1
        pi_blaster(channel_to_pin(channel), current_percentage + (change_per_increment * x))

    fishPI.services.database.save_meta(light_channel_meta(channel),percentage)
    return True

def flash_channel(channel):
        pi_blaster(channel_to_pin(channel), 0)
        pi_blaster(channel_to_pin(channel), 100)
        pi_blaster(channel_to_pin(channel), 0)

def pi_blaster(pin,percentage):
    v = (percentage / 100)
    with open('/dev/pi-blaster', 'w') as printer:
        printer.write("{} = {}".format(pin,v))

