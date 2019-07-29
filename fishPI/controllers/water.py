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
