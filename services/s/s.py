#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Service S checks the status of a customer"""

import logging
from logging.handlers import RotatingFileHandler
import pprint
import os
import sys
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
import config
import pymysql

# Initialise Flask
app = Flask(__name__)
app.debug = True

# Affect app logger to a global variable so logger can be used elsewhere.
config.logger = app.logger


@app.route("/status/<int:sid>", methods=["GET"])
def api_check(sid):
    """
    Check the status for user <id>

    :type sid : int
    """
    config.logger.info("*** Checking user id %d ***", sid)

    return_code = 200
    data = ""

    try:
        db = db_login()
        config.logger.info("Connection to database SUCCESSFUL")
        # Check database if user id exists.
        cursor = db.cursor()
        cursor.execute("SELECT NULL FROM player_status WHERE id= %s", str(sid))
    except Exception as e:
        config.logger.critical("Error while querying database : " + str(e.args[0]))
        return_code = 500

    if (return_code != 500):
        # fill the payload
        data = {}
        config.logger.info("%d matches for id %d", cursor.rowcount, sid)
        if cursor.rowcount == 0:
            data["status"] = "open"
        else:
            data["status"] = "played"

    # Send the status back
    resp = jsonify(data)
    resp.status_code = return_code
    config.logger.info("*** End checking user id %d ***", sid)
    add_headers(resp)
    return resp


@app.route("/status/<int:sid>", methods=["PUT"])
def api_add(sid):
    """
    Add the user <id> to the played database

    :type sid : int
    """
    config.logger.info("*** Tagging user id %d as played ***", sid)
    return_code = 200

    try:
        db = db_login()
        config.logger.info("Connection to database SUCCESSFUL")
        # Insert the user id in database
        cursor = db.cursor()
        cursor.execute("INSERT INTO player_status VALUES (%s)", str(sid))
        # db.commit()
    except Exception as e:
        config.logger.critical("Error while updating database : " + str(e.args[0]))
        return_code = 500
        pass

    # Acknowledge
    resp = make_response()
    resp.status_code = return_code
    config.logger.info("*** User id %d successfully tagged as played ***", sid)
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


def db_login():
    """Init database connection from configuration"""
    return pymysql.connect(host=config.s.conf_file.get_db_host(),
                           port=int(config.s.conf_file.get_db_port()),
                           user=config.s.conf_file.get_db_username(),
                           password=config.s.conf_file.get_db_password(),
                           database=config.s.conf_file.get_db_database(),
                           autocommit=True)


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
    if config.s.conf_file.get_s_debug().title() == 'True':
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
