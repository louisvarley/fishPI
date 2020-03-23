import fishPI
from fishPI import logging, services
from fishPI.services import co2
from flask import Flask, jsonify, request

@fishPI.app.route('/api/co2/setCo2OffHour/', methods=['GET'])
@fishPI.load("co2","setCo2OffHour")  
def set_co2_off_hour():
    hour = request.args.get('hour')
    fishPI.services.co2.set_co2_off_hour(hour)
    return jsonify(response="success")

@fishPI.app.route('/api/co2/setCo2OnHour/', methods=['GET'])
@fishPI.load("co2","setCo2OnHour")  
def set_co2_on_hour():
    hour = request.args.get('hour')
    fishPI.services.co2.set_co2_on_hour(hour)
    return jsonify(response="success")

@fishPI.app.route('/api/co2/getCo2OffHour/', methods=['GET'])
@fishPI.load("co2","getCo2OffHour")  
def get_co2_off_hour():
    return jsonify(
        hour=fishPI.services.co2.get_co2_off_hour().value
    )
    return jsonify(response=fishPI.services.co2.get_co2_off_hour())

@fishPI.app.route('/api/co2/getCo2OnHour/', methods=['GET'])
@fishPI.load("co2","getCo2OnHour")  
def get_co2_on_hour():
    return jsonify(
        hour=fishPI.services.co2.get_co2_on_hour().value
    )

@fishPI.app.route('/api/co2/setCo2On/', methods=['GET'])
@fishPI.load("co2","setCo2On")  
def set_co2_on():
    fishPI.services.co2.set_co2_on()
    return jsonify(response="success")

@fishPI.app.route('/api/co2/setCo2Off/', methods=['GET'])
@fishPI.load("co2","setCo2Off")  
def set_co2_off():
    fishPI.services.co2.set_co2_off()
    return jsonify(response="success")


@fishPI.app.route('/api/co2/doCo2Schedule/', methods=['GET'])
@fishPI.load("co2","doCo2Schedule")  
def do_co2_schedule():
    fishPI.services.co2.do_co2_schedule()
    return jsonify(response="success")

@fishPI.app.route('/api/co2/getCo2Status/', methods=['GET'])
@fishPI.load("co2","getCo2Status")
def get_co2_status():
    return jsonify(response=fishPI.services.co2.get_co2_status())
