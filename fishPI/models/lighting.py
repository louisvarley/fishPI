import json

class schedule():

    _1 = 0
    _2 = 0
    _3 = 0
    _4 = 0
    _5 = 0
    _6 = 0
    _7 = 0
    _8 = 0
    _9 = 0
    _9 = 0
    _10 = 0
    _11 = 0
    _12 = 0
    _13 = 0
    _14 = 0
    _15 = 0
    _16 = 0
    _17 = 0
    _18 = 0
    _19 = 0
    _20 = 0
    _21 = 0
    _22 = 0
    _23 = 0

    def __init__(self, json = None):
        for i in range(24):
            setattr(self, str(i), 0)

        if(json != None):
            schedule = json.loads(json)
            for i in range(23):
                setattr(self, str(i), schedule[i])

    def as_json(self):
        return json.dumps(self.__dict__)



class log():

    _1 = 0
    _2 = 0
    _3 = 0
    _4 = 0
    _5 = 0
    _6 = 0
    _7 = 0
    _8 = 0
    _9 = 0
    _9 = 0
    _10 = 0
    _11 = 0
    _12 = 0
    _13 = 0
    _14 = 0
    _15 = 0
    _16 = 0
    _17 = 0
    _18 = 0
    _19 = 0
    _20 = 0
    _21 = 0
    _22 = 0
    _23 = 0

    def __init__(self, json = None):
        for i in range(24):
            setattr(self, str(i), 0)

        if(json != None):
            log = json.loads(json)
            for i in range(23):
                setattr(self, str(i), log[i])

    def as_json(self):
        return json.dumps(self.__dict__)

