import json

from fishPI import models

class light_schedule():


    channel = None
    schedule = models.hour_schedule.hour_schedule()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)