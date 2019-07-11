import fishPI
from fishPI import logging, services
from fishPI.services import lighting

from flask import Flask, jsonify, request

class lighting():
    @fishPI.app.route('/lighting/getBrightness/', methods=['GET'])
    @fishPI.load("lighting","getBrightness")  
    def get_brightness():

        channel = request.args.get('channel')

        return jsonify(
            channel=channel,
            brightness=100
        )