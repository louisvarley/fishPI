import fishPI
from fishPI import logging, services
from fishPI.services import water
from flask import Flask, jsonify, request, json

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

@fishPI.app.route('/api/water/setWaterScheduleLitres/', methods=['POST'])
@fishPI.load("water","setWaterScheduleLitres")  
def set_water_schedule_litres():
    schedule = request.form.get('schedule')
    fishPI.services.water.set_water_schedule_litres(schedule)
    return jsonify(response="success")

@fishPI.app.route('/api/water/getWaterScheduleLitres/', methods=['GET'])
@fishPI.load("water","getWaterScheduleLitres")  
def get_water_schedule_litres():
    schedule = fishPI.services.water.get_water_schedule_litres()
    return jsonify(
        schedule=schedule.value,
        updated=schedule.added
    )

@fishPI.app.route('/api/water/getWaterScheduleTicks/', methods=['GET'])
@fishPI.load("water","getWaterScheduleTicks")  
def get_water_schedule_ticks():
    schedule = fishPI.services.water.get_water_schedule_ticks()
    return jsonify(
        schedule=json.loads(schedule.value),
        updated=schedule.added
    )

@fishPI.app.route('/api/water/getWaterLog/', methods=['GET'])
@fishPI.load("water","getWaterLog")  
def get_water_log():
    log = fishPI.services.water.get_log()
    return jsonify(
        log=json.loads(log.value),
        updated=log.added
    )

@fishPI.app.route('/api/water/getWaterTotalTicks/', methods=['GET'])
@fishPI.load("water","getWaterTotalTicks")  
def get_water_total_ticks():
    ticks = fishPI.services.water.get_water_total_ticks()
    return jsonify(
        ticks=ticks.value,
        updated=ticks.added
    )

@fishPI.app.route('/api/water/getWaterTotalLitres/', methods=['GET'])
@fishPI.load("water","getWaterTotalLitres")  
def get_water_total_litres():
    return jsonify(
        litres=fishPI.services.water.get_water_total_litres()
    )

@fishPI.app.route('/api/water/getWaterTotalHourLitres/', methods=['GET'])
@fishPI.load("water","getWaterTotalHourLitres")  
def get_water_total_hour_litres():
    return jsonify(
        litres=fishPI.services.water.get_water_total_hour_litres()
    )

@fishPI.app.route('/api/water/getWaterTotalHourTicks/', methods=['GET'])
@fishPI.load("water","getWaterTotalHourTicks")  
def get_water_total_hour_ticks():
    return jsonify(
        ticks=fishPI.services.water.get_water_total_hour_ticks()
    )


@fishPI.app.route('/api/water/getWaterTotalDayLitres/', methods=['GET'])
@fishPI.load("water","getWaterTotalDayLitres")  
def get_water_total_day_litres():
    return jsonify(
        litres=fishPI.services.water.get_water_total_day_litres()
    )

@fishPI.app.route('/api/water/getWaterLitresRemainingHour/', methods=['GET'])
@fishPI.load("water","getWaterLitresRemainingHour")  
def get_water_litres_remaining_hour():
    return jsonify(
        litres=fishPI.services.water.get_water_litres_remaining_hour()
    )

@fishPI.app.route('/api/water/getWaterTicksRemainingHour/', methods=['GET'])
@fishPI.load("water","getWaterTicksRemainingHour")  
def get_water_ticks_remaining_hour():
    return jsonify(
        litres=fishPI.services.water.get_water_ticks_remaining_hour()
    )

@fishPI.app.route('/api/water/getWaterLitresRemainingDay/', methods=['GET'])
@fishPI.load("water","getWaterLitresRemainingDay")  
def get_water_litres_remaining_day():
    return jsonify(
        litres=fishPI.services.water.get_water_litres_remaining_day()
    )

@fishPI.app.route('/api/water/getWaterTicksRemainingDay/', methods=['GET'])
@fishPI.load("water","getWaterTicksRemainingDay")  
def get_water_ticks_remaining_day():
    return jsonify(
        litres=fishPI.services.water.get_water_ticks_remaining_day()
    )

@fishPI.app.route('/api/water/doWaterSchedule/', methods=['GET'])
@fishPI.load("water","doWaterSchedule")  
def do_water_schedule():
    fishPI.services.water.do_water_schedule()   
    return jsonify(response="success")
  
