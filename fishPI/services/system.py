import fishPI
import random
import os
import re

from fishPI import logging
from fishPI import services
from fishPI import models


def load():
  load = None

def get_system_temperature():
   
    if(os.path.isfile("/opt/vc/bin/vcgencmd")):
        res = os.popen('vcgencmd measure_temp').readline()
        temperature = float((res.replace("temp=","").replace("'C\n","")))

        label = "normal"
        max = fishPI.config.load_from_config("temperature_warning","system_max")
        if(temperature > float(max)): label = "over"

    else:
        temperature = "-"
        label = "error"



    
    return {"label": label, "temperature": temperature}
