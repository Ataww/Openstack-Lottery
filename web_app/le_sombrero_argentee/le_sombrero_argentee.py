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
import config

# Initialise Flask
app = Flask(__name__)
app.debug = True

# Affect app logger to a global variable so logger can be used elsewhere.
config.logger = app.logger

@app.route('/', methods=['GET'])
def get_index(id):
    pass

def configure_logger(logger, logfile):
    """Configure logger"""
    formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)s :: %(message)s")
    file_handler = RotatingFileHandler(logfile, "a", 1000000, 1)

    # Add logger to file
    if (config.site.conf_file.get_site_debug().title() == 'True'):
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
