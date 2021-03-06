# coding=utf-8

import configparser

# Initialise global variable
logger = None
i = None


def initialise_i():
    """Define  global object so it can be called from anywhere."""
    global i
    i = I()


class I(object):
    def __init__(self):
        self.NAME = "Microservice I"
        self.VERSION = "0.1"
        #
        # Configuration file
        self.conf_file = iConfiguration("i.conf")


class iConfiguration(object):

    def __init__(self, configuration_file):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(configuration_file)

    def get_i_port(self):
        return self.config.get("i", "port")

    def get_i_tmpfile(self):
        return self.config.get("i", "tmpfile")

    def get_i_tempo(self):
        return self.config.get("i", "tempo")

    def get_i_debug(self):
        return self.config.get("i", "debug")

    def get_i_db_host(self):
        return self.config.get("db", "host")

    def get_i_db_port(self):
        return self.config.get("db", "port")

    def get_i_db_user(self):
        return self.config.get("db", "user")

    def get_i_db_pwd(self):
        return self.config.get("db", "pwd")

    def get_i_db_name(self):
        return self.config.get("db", "name")
