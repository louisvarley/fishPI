import fishPI
from fishPI import logging, services
from fishPI.services import ambients
from flask import Flask, jsonify, request

@fishPI.app.route('/api/ambients/getAmbients/', methods=['GET'])
@fishPI.load("ambients","getAmbients")  
def get_ambients():

    ambients = fishPI.services.ambients.get_ambients()
    return jsonify(
        type=ambients.value,
        updated=ambients.added
    )


@fishPI.app.route('/api/ambients/getLightingOverride/', methods=['GET'])
@fishPI.load("ambients","getLightingOverride")  
def get_lighting_override():

    override = fishPI.services.ambients.get_lighting_override()
    return jsonify(
        override=override.value,
        updated=override.added
    )

@fishPI.app.route('/api/ambients/getAmbientsStatus/', methods=['GET'])
@fishPI.load("ambients","getAmbientsStatus")  
def get_ambients_status():

    status = fishPI.services.ambients.get_ambients_status()
    return jsonify(
        status=status.value,
        updated=status.added
    )

@fishPI.app.route('/api/ambients/setAmbientsNone/', methods=['GET'])
@fishPI.load("ambients","setAmbientsNone")  
def set_ambients_none():
    fishPI.services.ambients.set_ambients_none()
    return jsonify({"response": "Success"})

@fishPI.app.route('/api/ambients/setAmbientsCloudy/', methods=['GET'])
@fishPI.load("ambients","setAmbientsCloudy")  
def set_ambients_cloudy():
    duration = request.args.get('duration')
    fishPI.services.ambients.set_ambients_cloudy(duration)
    return jsonify({"response": "Success"})

@fishPI.app.route('/api/ambients/setAmbientsRainy/', methods=['GET'])
@fishPI.load("ambients","setAmbientsRainy")  
def set_ambients_rainy():
    duration = request.args.get('duration')
    fishPI.services.ambients.set_ambients_rainy(duration)
    return jsonify({"response": "Success"})

@fishPI.app.route('/api/ambients/setAmbientsStormy/', methods=['GET'])
@fishPI.load("ambients","setAmbientsStormy")  
def set_ambients_stormy():
    duration = request.args.get('duration')
    fishPI.services.ambients.set_ambients_stormy(duration)
    return jsonify({"response": "Success"})

@fishPI.app.route('/api/ambients/setAmbientsNature/', methods=['GET'])
@fishPI.load("ambients","setAmbientsNature")  
def set_ambients_nature():
    duration = request.args.get('duration')
    fishPI.services.ambients.set_ambients_nature(duration)
    return jsonify({"response": "Success"})

