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
from flask import jsonify
import config
import pymysql

# Initialise Flask
app = Flask(__name__)
app.debug = True

# Affect app logger to a global variable so logger can be used elsewhere.
config.logger = app.logger

@app.route('/Ident/<int:id>', methods=['GET'])
def get_user(id):

    config.logger.info("Recieved request to find user with ID %d", id)
    return_code = 200

    try:
        db = pymysql.connect(host=config.i.conf_file.get_i_db_host()
                             , port=int(config.i.conf_file.get_i_db_port())
                             , user=config.i.conf_file.get_i_db_user()
                             , password=config.i.conf_file.get_i_db_pwd()
                             , database=config.i.conf_file.get_i_db_name())
        config.logger.info("Connection to database SUCCEED")
    except Exception as e:
        config.logger.critical("Error while connecting to database : " + e.args[1])
        return_code = 500
        pass

    if return_code == 200:
        cursor = db.cursor()
        try:
            cursor.execute('SELECT id_customer, firstname, lastname, email FROM ps_customer WHERE id_customer = ' + str(id))
            config.logger.info("Request to databse SUCCEED")
        except Exception as e:
            config.logger.critical("Error while requesting database: " + e.args[1])
            return_code = 500
            pass

    data = {}
    if return_code == 200:
        for row in cursor:
            data["id"] = row[0]
            data["firstname"] = row[1]
            data["lastname"] = row[2]
            data["email"] = row[3]

    resp = jsonify(data)
    resp.status_code = return_code
    config.logger.info("*** End processing for user with id %s ***", id)
    add_headers(resp)
    return resp

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
    if (config.i.conf_file.get_i_debug().title() == 'True'):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

if __name__ == "__main__":
    # Vars
    app_logfile = "i.log"

    # Change diretory to script one
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except FileNotFoundError:
        pass

    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)

    # Initialise apps
    config.initialise_i()

    # Configure Flask logger
    configure_logger(app.logger, app_logfile)

    config.logger.info("Starting %s", config.i.NAME)
    app.run(port=int(config.i.conf_file.get_i_port()), host='0.0.0.0')
