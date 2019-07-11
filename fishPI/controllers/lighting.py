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
            brightness=fishPI.services.lighting.get_brightness(channel)
        )

    @fishPI.app.route('/lighting/setBrightness/', methods=['GET'])
    @fishPI.load("lighting","setBrightness")  
    def set_brightness():

        channel = request.args.get('channel')
        percentage = request.args.get('percentage')

        fishPI.services.lighting.set_brightness(channel,percentage)

        return True