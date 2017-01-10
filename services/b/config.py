# coding=utf-8

import configparser

# Initialise global variable
logger = None
b = None


def initialise_b():
    """Define b global object so it can be called from anywhere."""
    global b
    b = B()


class B(object):
    def __init__(self):
        self.NAME = "Microservice b"
        self.VERSION = "0.1"
        #
        # Configuration file
        self.conf_file = bConfiguration("b.conf")


class bConfiguration(object):

    def __init__(self, configuration_file):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(configuration_file)

    def get_b_port(self):
        return self.config.get("b", "port")

    def get_b_tmpfile(self):
        return self.config.get("b", "tmpfile")

    def get_b_tempo(self):
        return self.config.get("b", "tempo")

    def get_b_debug(self):
        return self.config.get("b", "debug")

    def get_swift_user(self):
        return self.config.get("swift", "user")

    def get_swift_password(self):
        return self.config.get("swift", "password")

    def get_swift_auth_url(self):
        return self.config.get("swift", "auth_url")

    def get_swift_user_domain_name(self):
        return self.config.get("swift", "user_domain_name")

    def get_swift_project_name(self):
        return self.config.get("swift", "project_name")

    def get_swift_project_id(self):
        return self.config.get("swift", "project_id")

    def get_s_host(self):
        return self.config.get("s", "host")

    def get_s_port(self):
        return self.config.get("s", "port")

    def get_s_service(self):
        return self.config.get("s", "service")

    def get_w_host(self):
        return self.config.get("w", "host")

    def get_w_port(self):
        return self.config.get("w", "port")

    def get_w_service(self):
        return self.config.get("w", "service")
