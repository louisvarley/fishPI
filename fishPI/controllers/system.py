import fishPI
from fishPI import logging, services
from fishPI.services import system
from flask import Flask, jsonify, request

@fishPI.app.route('/api/system/getSystemTemperature/', methods=['GET'])
@fishPI.load("system","getSystemTemperature")  
def get_system_temperature():

    return jsonify(fishPI.services.system.get_system_temperature())

@fishPI.app.route('/api/system/online/', methods=['GET'])
@fishPI.load("system","online")  
def online():

    return jsonify({"response": True})



