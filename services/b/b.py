#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Service B launch the lotery and send the price to web server"""

import base64
import logging
import os
import pprint
import random
import subprocess
import sys
import time
from flask import Flask
from flask import jsonify
from flask import request
import requests
from logging.handlers import RotatingFileHandler
import json

import config

# Initialise Flask
app = Flask(__name__)
app.debug = True

# Affect app logger to a global variable so logger can be used elsewhere.
config.logger = app.logger


@app.route("/play/<id>")
def api_play(id):
    """Get the price for user <id>"""
    config.logger.info("*** Start processing id %s ***", id)

    # Call Web service w
    request_data = requests.get("http://localhost:8090/play/"+id)

    if(request_data.status_code == requests.codes.ok):
        data = {"price": getValueJson("price",request_data.json()), "img": getValueJson("img",request_data.json())}
        resp = jsonify(data)
        resp.status_code = requests.codes.ok
    else:
        resp = jsonify("")
        resp.status_code = request_data.status_code

    config.logger.info("*** End processing id %s ***", id)
    add_headers(resp)
    return resp

def getValueJson(keyResearch, data):
    for key, value in data.items():
        if keyResearch in key:
            return value
    return ""

@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Shutdown server"""
    shutdown_server()
    config.logger.info("Stopping %s...", config.b.NAME)
    return "Server shutting down..."


@app.route("/", methods=["GET"])
def api_root():
    """Root url, provide service name and version"""
    data = {
        "Service": config.b.NAME,
        "Version": config.b.VERSION
    }

    resp = jsonify(data)
    resp.status_code = 200

    resp.headers["AuthorSite"] = "https://github.com/uggla/openstack_lab"

    add_headers(resp)
    return resp

def shutdown_server():
    """shutdown server"""
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


def configure_logger(logger, logfile):
    """Configure logger"""
    formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)s :: %(message)s")
    file_handler = RotatingFileHandler(logfile, "a", 1000000, 1)

    # Add logger to file
    if (config.b.conf_file.get_b_debug().title() == 'True'):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')


if __name__ == "__main__":
    # Vars
    app_logfile = "b.log"

    # Change diretory to script one
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except FileNotFoundError:
        pass

    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)

    # Initialise apps
    config.initialise_b()

    # Configure Flask logger
    configure_logger(app.logger, app_logfile)

    config.logger.info("Starting %s", config.b.NAME)
    app.run(port=int(config.b.conf_file.get_b_port()), host='0.0.0.0')
