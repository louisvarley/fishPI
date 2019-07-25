
import fishPI
from fishPI import logging, services
from fishPI.services import temperature
from flask import Flask, jsonify, request

@fishPI.app.route('/api/temperature/getTemperature/', methods=['GET'])
@fishPI.load("temperature","getTemperature")  
def get_temperature():

    return jsonify(fishPI.services.temperature.get_temperature())