import fishPI
from fishPI import logging, services
from fishPI.services import lighting
from flask import Flask, jsonify, request

@fishPI.app.route('/lighting/getBrightness/', methods=['GET'])
@fishPI.load("lighting","getBrightness")  
def get_brightness():

    channel = request.args.get('channel')
    brightness = fishPI.services.lighting.get_brightness(channel)

    return jsonify(
        channel=channel,
        percentage=brightness.value,
        updated=brightness.added
    )

@fishPI.app.route('/lighting/setBrightness/', methods=['GET'])
@fishPI.load("lighting","setBrightness")  
def set_brightness():

    channel = request.args.get('channel')
    percentage = request.args.get('percentage')

    brightness = fishPI.services.lighting.set_brightness(channel,percentage)

    return jsonify(
        channel=channel,
        percentage=brightness.value,
        updated=brightness.added
    )

@fishPI.app.route('/lighting/getSchedule/', methods=['GET'])
@fishPI.load("lighting","getSchedule")  
def get_schedule():

    channel = request.args.get('channel')
    schedule = fishPI.services.lighting.get_schedule(channel)

    return jsonify(
        channel=channel,
        schedule=schedule.value,
        updated=schedule.added
    )
