import fishPI
from fishPI import logging, services
from fishPI.services import water
from flask import Flask, jsonify, request

@fishPI.app.route('/api/water/setSolenoidOn/', methods=['GET'])
@fishPI.load("water","setSolenoidOn")  
def set_solenoid_on():
    fishPI.services.water.set_solenoid_on()
    return jsonify(response="success")


@fishPI.app.route('/api/water/setSolenoidOff/', methods=['GET'])
@fishPI.load("water","setSolenoidOff")  
def set_solenoid_off():
    fishPI.services.water.set_solenoid_off()
    return jsonify(response="success")

@fishPI.app.route('/api/water/getSolenoidStatus/', methods=['GET'])
@fishPI.load("water","getSolenoidStatus")
def get_solenoid_status():
    return jsonify(response=fishPI.services.water.get_solenoid_status())

@fishPI.app.route('/api/water/getWaterSchedule/', methods=['GET'])
@fishPI.load("water","getWaterSchedule")  
def get_water_schedule():
    schedule = fishPI.services.water.get_water_schedule()
    return jsonify(
        schedule=schedule.value,
        updated=schedule.added
    )

@fishPI.app.route('/api/water/setWaterSchedule/', methods=['POST'])
@fishPI.load("water","setWaterSchedule")  
def set_water_schedule():
    schedule = request.form.get('schedule')
    fishPI.services.water.set_water_schedule(schedule)
    return jsonify(response="success")

@fishPI.app.route('/api/water/getWaterLog/', methods=['GET'])
@fishPI.load("water","getWaterLog")  
def get_water_log():
    log = fishPI.services.water.get_log()
    return jsonify(
        log=log.value,
        updated=log.added
    )

@fishPI.app.route('/api/water/getWaterTicks/', methods=['POST'])
@fishPI.load("water","getWaterTicks")  
def get_water_ticks():
    ticks = fishPI.services.water.get_water_ticks()
    return jsonify(
        ticks=ticks.value,
        updated=ticks.added
    )

@fishPI.app.route('/api/water/getWaterTotal/', methods=['POST'])
@fishPI.load("water","getWaterTotal")  
def get_litres_total():
    return jsonify(
        litres=fishPI.services.water.get_water_total()
    )

@fishPI.app.route('/api/water/getWaterHour/', methods=['GET'])
@fishPI.load("water","getWaterHour")  
def get_hour_litres():
    return jsonify(
        litres=fishPI.services.water.get_water_hour()
    )


@fishPI.app.route('/api/water/getWaterDay/', methods=['GET'])
@fishPI.load("water","getWaterDay")  
def get_day_litres():
    return jsonify(
        litres=fishPI.services.water.get_water_day()
    )

@fishPI.app.route('/api/water/updateWaterHour/', methods=['GET'])
@fishPI.load("water","updateWaterHour")  
def update_hour_litres():
    return jsonify(
        litres=fishPI.services.water.update_water_hour()
    )

@fishPI.app.route('/api/water/getWaterRemainingThisHour/', methods=['GET'])
@fishPI.load("water","getWaterRemainingThisHour")  
def get_water_remaining_this_hour():
    return jsonify(
        litres=fishPI.services.water.get_water_remaining_this_hour()
    )

@fishPI.app.route('/api/water/getWaterRemainingThisDay/', methods=['GET'])
@fishPI.load("water","getWaterRemainingThisDay")  
def get_water_remaining_this_day():
    return jsonify(
        litres=fishPI.services.water.get_water_remaining_this_day()
    )

@fishPI.app.route('/api/water/doWaterSchedule/', methods=['GET'])
@fishPI.load("water","doWaterSchedule")  
def do_water_schedule():

    fishPI.services.water.do_water_schedule()   
    return jsonify(response="success")
  
