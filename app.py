#!/usr/bin/env python3

import fishPI, subprocess, os, platform, ssl, sys, glob, ntpath, atexit

from fishPI import config, logging
from time import sleep
from os import environ
from urllib.request import urlopen
from flask import Flask, redirect, render_template
from flasgger.utils import swag_from
from flasgger import Swagger
from multiprocessing import Process, Queue
from apscheduler.schedulers.background import BackgroundScheduler


#Here is listed any internal scheduled jobs
def schedulers():

    from fishPI.services import temperature, lighting, water

    temperatureScheduler = BackgroundScheduler()
    temperatureScheduler.add_job(func=temperature.log_temperature, trigger="interval", seconds=60)
    temperatureScheduler.start()

    lightingScheduler = BackgroundScheduler()
    lightingScheduler.add_job(func=lighting.do_schedule, trigger="interval", seconds=60)
    lightingScheduler.start()
    lighting.do_schedule()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: temperatureScheduler.shutdown())
    atexit.register(lambda: lightingScheduler.shutdown())


# Methods called LOAD will run everytime the app is started, for pre-filling database etc 
def service_loaders():

    from fishPI import services

    services.database.load()

    modules = glob.glob(os.path.join(fishPI.config.app_dir,"services","*.py"))
    for module in modules:
        fullModule = "fishPI.services." + ntpath.basename(module).replace(".py","")
        i = __import__(fullModule, globals(), locals()) # returns module object
        if hasattr(i, 'load'):
            try:
                eval(fullModule + '.load()')
            except Exception as e:
                logging.logInfo(" * Loading Service onLoad for " + fullModule + " FAILED : " + str(e))

def before_launch():
    @fishPI.app.route('/api')
    def root():
        return redirect("/apidocs/", code=302)

    @fishPI.app.route('/')
    def render_static():
        return render_template("index.html")

def main():
    #Pre-Set Config 
    fishPI.config.working_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    fishPI.config.app_dir = os.path.join(fishPI.config.working_dir,"fishPI")
    fishPI.config.template_dir = os.path.join(fishPI.config.app_dir,"templates")
    fishPI.config.static_dir = os.path.join(fishPI.config.app_dir,"static")
    fishPI.config.version = fishPI.config.get_version()
    fishPI.config.host_name = str(platform.uname()[1])
    fishPI.config.host = environ.get('SERVER_HOST', '0.0.0.0')
    fishPI.config.database = os.path.join(fishPI.config.working_dir,fishPI.config.load_from_config("instance","database_file_name"))
    fishPI.config.log_dir = os.path.join(fishPI.config.working_dir,"logs")

    #INI File Config
    fishPI.config.title = fishPI.config.load_from_config("instance","title")
    fishPI.config.ui_version = fishPI.config.load_from_config("instance","swagger_ui_version")
    fishPI.config.port = fishPI.config.load_from_config("instance","port");
    fishPI.config.light_pins = fishPI.config.load_from_config("light_pins")

    fishPI.config.solenoid_pin = fishPI.config.load_from_config("plug_pins","solenoid")
    fishPI.config.rain_pin = fishPI.config.load_from_config("plug_pins","rain")

    ssl._create_default_https_context = ssl._create_unverified_context

    fishPI.app = Flask(__name__,template_folder=fishPI.config.template_dir,static_folder = fishPI.config.static_dir)

    #Used for Loading YAMLS
    fishPI.load = lambda controller, definition: swag_from(os.path.join(fishPI.config.app_dir, "yaml", controller, definition + ".yaml"))

    fishPI.app.config['SWAGGER'] = {
        'uiversion': fishPI.config.ui_version,
        'title': fishPI.config.title,
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
        "specs": [
            {
                "version":fishPI.config.get_full_version(),
                "title": fishPI.config.host_name,
                "endpoint": 'v1_spec',
                "description": "FishPI API",
                "route": '/spec.json',
            }
        ]
    }

    Swagger(fishPI.app)
    before_launch()

    user = os.getenv("SUDO_USER")

    #Import all views, controllers, models and services 
    from fishPI import views, controllers, models, services

    #Runs Service Loaders
    logging.logInfo(" * Running Service Loaders")
    service_loaders()
    
    #Runs AP Schedulers 
    logging.logInfo(" * Starting Schedulers") 
    schedulers()

    #Run FishPI / Flask
    logging.logInfo(" * Starting " + fishPI.config.title + " [" + fishPI.config.host + ":" + str(fishPI.config.port) + "]")
    fishPI.app.run(host=fishPI.config.host, port=fishPI.config.port, debug=True)

if __name__ == '__main__':
    main()

