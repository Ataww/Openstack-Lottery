#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Service I check if user exist in database
   If he doesn't, he create it
"""

import logging
from logging.handlers import RotatingFileHandler
import pprint
import os
import sys
from flask import Flask
from flask import render_template
import config
import requests
from flask import Response

# Initialise Flask
app = Flask(__name__)
app.debug = True

# Affect app logger to a global variable so logger can be used elsewhere.
config.logger = app.logger


@app.route('/<int:id>')
def index(id):
    config.logger.info("Recieved request with ID %d", id)

    render_option = {}
    render_option["title"] = config.site.NAME
    render_option["url"] = "http://localhost:" + config.site.conf_file.get_site_port() + "/"
    render_option["id"] = str(id)

    config.logger.info("Launch render on template index.html")
    return render_template('index.html', render_option=render_option)

@app.route('/ident/<int:id>')
def ident_user(id):
    host_i = config.site.conf_file.get_site_i_host()
    port_i = config.site.conf_file.get_site_i_port()
    service_i = config.site.conf_file.get_site_i_service()
    request_data = requests.get("http://" + host_i + ":" + port_i + "/" + service_i + "/" + str(id))
    response = Response(request_data)
    add_headers(response)
    return response

@app.route('/image/<int:id>')
def image_user(id):
    host_p = config.site.conf_file.get_site_p_host()
    port_p = config.site.conf_file.get_site_p_port()
    service_p = config.site.conf_file.get_site_p_service()
    request_data = requests.get("http://" + host_p + ":" + port_p + "/" + service_p + "/" + str(id))
    response = Response(request_data)
    add_headers(response)
    return response

@app.route('/status/<int:id>')
def status_user(id):
    host_s = config.site.conf_file.get_site_s_host()
    port_s = config.site.conf_file.get_site_s_port()
    service_s = config.site.conf_file.get_site_s_service()
    request_data = requests.get("http://" + host_s + ":" + port_s + "/" + service_s + "/" + str(id))
    response = Response(request_data)
    add_headers(response)
    return response

@app.route('/play/<int:id>')
def play_button(id):
    host_b = config.site.conf_file.get_site_b_host()
    port_b = config.site.conf_file.get_site_b_port()
    service_b = config.site.conf_file.get_site_b_service()
    request_data = requests.get("http://" + host_b + ":" + port_b + "/" + service_b + "/" + str(id))
    response = Response(request_data)
    add_headers(response)
    return response

def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')

def configure_logger(logger, logfile):
    """Configure logger"""
    formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)s :: %(message)s")
    file_handler = RotatingFileHandler(logfile, "a", 1000000, 1)

    # Add logger to file
    if config.site.conf_file.get_site_debug().title() == 'True':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


if __name__ == "__main__":
    # Vars
    app_logfile = "le_sombrero_argentee.log"

    # Change diretory to script one
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except FileNotFoundError:
        pass

    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)

    # Initialise apps
    config.initialise_site()

    # Configure Flask logger
    configure_logger(app.logger, app_logfile)

    config.logger.info("Starting %s", config.site.NAME)
    app.run(port=int(config.site.conf_file.get_site_port()), host='0.0.0.0')
