import fishPI
import os.path
import os, random
import subprocess
import time, datetime, json
import simpleaudio

from datetime import datetime  
from datetime import timedelta  

from fishPI import logging
from fishPI import services
from fishPI import models
from fishPI import config

def load():
    services.database.set_initial("lighting_override",0)
    services.database.set_initial("ambients_type","none")
    services.database.set_initial("ambients_duration",0)
    services.database.set_initial("ambients_status","off")

def set_lighting_override(percentage):
        services.database.set_meta("lighting_override",str(percentage))

def set_ambients_cloudy(duration = 10):
    set_ambients("cloudy", duration)
    set_lighting_override(20)

def set_ambients_stormy(duration = 10):
    set_ambients("stormy", duration)
    set_lighting_override(5)

def set_ambients_rainy(duration = 10):
    set_ambients("rainy", duration)
    set_lighting_override(50)

def set_ambients_nature(duration = 10):
    set_ambients("nature", duration)

def set_ambients_none():
    set_ambients("none", 0)
    set_lighting_override(0)
    set_ambients_status("off")
    simpleaudio.stop_all()

def set_ambients(ambient, duration = 0):
    services.database.set_meta("ambients_type",ambient)
    services.database.set_meta("ambients_duration",duration)

def get_ambients():
    return services.database.get_meta("ambients_type")

def get_lighting_override():
    return services.database.get_meta("lighting_override")

def get_ambients_status():
    return services.database.get_meta("ambients_status")

def set_ambients_status(status):
    return services.database.set_meta("ambients_status", status)

def play_random_sfx(sounds_dir):
    if(os.path.exists(sounds_dir)):

        while True:
            file = random.choice(os.listdir(sounds_dir)) 
            if( 'background' not in file ):
                    break

        file_path = os.path.join(fishPI.config.app_dir, "sounds", get_ambients().value, file)
        print("playing " + file_path)
        wave_obj = simpleaudio.WaveObject.from_wave_file(background_file_path)
        play_obj = wave_obj.play()

def play_random_background(sounds_dir):
    if(os.path.exists(sounds_dir)):

        while True:
            file = random.choice(os.listdir(sounds_dir)) 
            if( 'background' in file ):
                    break

        file_path = os.path.join(fishPI.config.app_dir, "sounds", get_ambients().value, file)
        print("playing " + file_path)
        wave_obj = simpleaudio.WaveObject.from_wave_file(background_file_path)
        play_obj = wave_obj.play()

def do_ambients():

    if(get_ambients_status().value == "on"): return False
    if(get_ambients().value == "none"): return False

    set_ambients_status("on")

    #DIR where sounds are found
    sounds_dir = os.path.join(fishPI.config.app_dir, "sounds", get_ambients().value)

    #Play random background track
    play_random_background(sounds_dir)

    #The Ambient Loop
    while( get_ambients_status().value == "on" or  get_ambients().value == "none"):

       if(get_ambients().value == "nature"):
                play_random_sfx(sounds_dir)
                time.sleep(random.randint(0, 5))

       if(get_ambients().value == "stormy"):
                play_random_sfx(sounds_dir)
                time.sleep(random.randint(0, 5))
   
def clear_ambients():

    set = services.database.get_meta("ambients_duration")
    if(int(set.value) > 0):

        clear_time = set.added + timedelta(minutes=int(set.value))  

        if(clear_time > datetime.now()):
            set_ambients("none",0) 
            set_lighting_override(0)
            set_ambients_status("off")
            simpleaudio.stop_all()