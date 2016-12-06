#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Service S checks the status of a customer"""

import logging
from logging.handlers import RotatingFileHandler
import pprint
import os
import random
import time
import subprocess
import sys
from flask import Flask
from flask import jsonify
from flask import request
import config

# Initialise Flask
app = Flask(__name__)
app.debug = True

# Affect app logger to a global variable so logger can be used elsewhere.
config.logger = app.logger


@app.route("/user/<id>", methods=["GET"])
def api_check(id):
    """Check the status for user <id>"""
    config.logger.info("*** Checking user id %s ***", id)

    # Check database if user id exists.
    # Here's where all the magic happen
    # Add latency on the service to simulate a long process
    time.sleep(int(config.s.conf_file.get_s_tempo()))

    # Send the status back
    data = {"id": id, "status": "played"}
    resp = jsonify(data)
    resp.status_code = 200
    config.logger.info("*** End checking user id %s ***", id)
    add_headers(resp)
    return resp


@app.route("/user", methods=["PUT"])
def api_add(id):
    """Add the user <id> to the played database"""
    config.logger.info("*** Tagging user id %s as played ***", id)
    # Insert the user id in database
    # Here's where all the magic happen

    # Acknowledge
    data = {"status": "ok"}
    resp = jsonify(data)
    resp.status_code = 200
    config.logger.info("*** User id %s successfully tagged as played ***", id)
    add_headers(resp)
    return resp


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Shutdown server"""
    shutdown_server()
    config.logger.info("Stopping %s...", config.s.NAME)
    return "Server shutting down..."


@app.route("/", methods=["GET"])
def api_root():
    """Root url, provide service name and version"""
    data = {
        "Service": config.s.NAME,
        "Version": config.s.VERSION
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
    if (config.s.conf_file.get_s_debug().title() == 'True'):
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
    app_logfile = "s.log"

    # Change diretory to script one
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except FileNotFoundError:
        pass

    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)

    # Initialise apps
    config.initialise_s()

    # Configure Flask logger
    configure_logger(app.logger, app_logfile)

    config.logger.info("Starting %s", config.s.NAME)
    app.run(port=int(config.s.conf_file.get_s_port()), host='0.0.0.0')
