import fishPI
from fishPI import logging, services
from fishPI.services import ambients
from flask import Flask, jsonify, request

@fishPI.app.route('/api/ambients/setAmbientsCloudy/', methods=['GET'])
@fishPI.load("ambients","setAmbientsCloudy")  
def set_ambients_cloudy():
    duration = request.args.get('duration')
    fishPI.services.ambients.set_ambients_cloudy(duration)
    return jsonify({"response": "Success"})



