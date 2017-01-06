#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Service P get the price image in SWIFT"""

import logging
import os
import sys
import pprint
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
import config
import swift

# Initialise Flask
app = Flask(__name__)
app.debug = True

# Affect app logger to a global variable so logger can be used elsewhere.
config.logger = app.logger


@app.route("/image/<id>")
def get_image(id):
    # data = {}
    # data["image"] = str(swift.getImage(id))

    # resp = jsonify(data)
    # resp.status_code = 200
    # add_headers(resp)
    # return resp
    data = swift.getImage(id)[1]
    print(data)
    return Response(data, mimetype='image/png')

def configure_logger(logger, logfile):
    """Configure logger"""
    formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)s :: %(message)s")
    file_handler = RotatingFileHandler(logfile, "a", 1000000, 1)

    # Add logger to file
    if (config.p.conf_file.get_p_debug().title() == 'True'):
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
    app_logfile = "p.log"

    # Change diretory to script one
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except FileNotFoundError:
        pass

    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)

    # Initialise apps
    config.initialise_p()

    # Configure Flask logger
    configure_logger(app.logger, app_logfile)

    config.logger.info("Starting %s", config.p.NAME)
    app.run(port=int(config.p.conf_file.get_p_port()), host='0.0.0.0')
