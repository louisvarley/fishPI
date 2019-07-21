import fishPI, subprocess, os, platform, ssl, sys

from fishPI import config, logging
from time import sleep
from os import environ
from urllib.request import urlopen
from flask import Flask, redirect, render_template
from flasgger.utils import swag_from
from flasgger import Swagger
from multiprocessing import Process, Queue

#http://symbiot4.creatingo.com/

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

    #INI File Config
    fishPI.config.title = fishPI.config.load_from_config("instance","title")
    fishPI.config.ui_version = fishPI.config.load_from_config("instance","swagger_ui_version")
    fishPI.config.port = fishPI.config.load_from_config("instance","port");
    fishPI.config.light_pins = fishPI.config.load_from_config("light_pins")

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

    logging.logInfo(" * Starting " + fishPI.config.title + " [" + fishPI.config.host + ":" + str(fishPI.config.port) + "]")

    #Import all views, controllers, models and services 
    from fishPI import views, controllers, models, services

    fishPI.app.run(host=fishPI.config.host, port=fishPI.config.port, debug=True)

if __name__ == '__main__':
    main()

