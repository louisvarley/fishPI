import fishPI
from fishPI import logging, services
from fishPI.services import temperature
from flask import Flask, jsonify, request

@fishPI.app.route('/api/temperature/getTemperature/', methods=['GET'])
@fishPI.load("temperature","getTemperature")  
def get_temperature():
    return jsonify(fishPI.services.temperature.get_temperature())

@fishPI.app.route('/api/temperature/logTemperature/', methods=['GET'])
@fishPI.load("temperature","logTemperature")  
def log_temperature():
    return jsonify(fishPI.services.temperature.log_temperature())

@fishPI.app.route('/api/temperature/getTemperatureLog/', methods=['GET'])
@fishPI.load("temperature","getTemperatureLog")  
def get_temperature_log():
    return jsonify(fishPI.services.temperature.get_temperature_log())