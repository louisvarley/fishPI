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
