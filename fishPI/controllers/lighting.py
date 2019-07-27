import fishPI
from fishPI import logging, services
from fishPI.services import lighting
from flask import Flask, jsonify, request

@fishPI.app.route('/api/lighting/getBrightness/', methods=['GET'])
@fishPI.load("lighting","getBrightness")  
def get_brightness():

    channel = request.args.get('channel')
    brightness = fishPI.services.lighting.get_brightness(channel)

    return jsonify(
        channel=channel,
        percentage=brightness.value,
        updated=brightness.added
    )

@fishPI.app.route('/api/lighting/setBrightness/', methods=['GET'])
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




@fishPI.app.route('/api/lighting/setBrightnessAll/', methods=['GET'])
@fishPI.load("lighting","setBrightnessAll")  
def set_brightness_all():

    percentage = request.args.get('percentage')
    fishPI.services.lighting.set_brightness_all(percentage)

    return jsonify(response="success")

@fishPI.app.route('/api/lighting/getSchedule/', methods=['GET'])
@fishPI.load("lighting","getSchedule")  
def get_schedule():

    channel = request.args.get('channel')
    schedule = fishPI.services.lighting.get_schedule(channel)

    return jsonify(
        channel=channel,
        schedule=schedule.value,
        updated=schedule.added
    )

@fishPI.app.route('/api/lighting/setSchedule/', methods=['POST'])
@fishPI.load("lighting","setSchedule")  
def set_schedule():

    channel = request.args.get('channel')
    schedule = request.form.get('schedule')

    fishPI.services.lighting.set_schedule(channel, schedule)

    return jsonify(response="success")

@fishPI.app.route('/api/lighting/flash/', methods=['GET'])
@fishPI.load("lighting","flash")  
def flash():

    channel = request.args.get('channel')
    fishPI.services.lighting.flash(channel)
    return jsonify(response="success")

@fishPI.app.route('/api/lighting/doSchedule/', methods=['GET'])
@fishPI.load("lighting","doSchedule")  
def do_schedule():

    fishPI.services.lighting.do_schedule()   
    return jsonify(response="success")