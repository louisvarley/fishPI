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

@fishPI.app.route('/api/water/getSchedule/', methods=['GET'])
@fishPI.load("water","getSchedule")  
def get_water_schedule():

    schedule = fishPI.services.water.get_schedule()

    return jsonify(
        schedule=schedule.value,
        updated=schedule.added
    )

@fishPI.app.route('/api/water/setSchedule/', methods=['POST'])
@fishPI.load("water","setSchedule")  
def set_water_schedule():

    schedule = request.form.get('schedule')
    fishPI.services.water.set_schedule(schedule)

    return jsonify(response="success")

@fishPI.app.route('/api/water/getFlowCount/', methods=['POST'])
@fishPI.load("water","getFlowCount")  
def get_flow_count():

    count = fishPI.services.water.get_flow_count()

    return jsonify(
        count=count.value,
        updated=count.added
    )


@fishPI.app.route('/api/water/getLitresTotal/', methods=['POST'])
@fishPI.load("water","getLitresTotal")  
def get_litres_total():

    return jsonify(
        litres=fishPI.services.water.get_litres_total()
    )

@fishPI.app.route('/api/water/getHourLitres/', methods=['GET'])
@fishPI.load("water","getHourLitres")  
def get_hour_litres():

    return jsonify(
        litres=fishPI.services.water.get_hour_litres()
    )


@fishPI.app.route('/api/water/getDayLitres/', methods=['GET'])
@fishPI.load("water","getDayLitres")  
def get_day_litres():

    return jsonify(
        litres=fishPI.services.water.get_day_litres()
    )


@fishPI.app.route('/api/water/updateHourLitres/', methods=['POST'])
@fishPI.load("water","updateHourLitres")  
def update_hour_litres():

    return jsonify(
        litres=fishPI.services.water.update_hour_litres()
    )
