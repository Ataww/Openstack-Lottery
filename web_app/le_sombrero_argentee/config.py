# coding=utf-8

import configparser

# Initialise global variable
logger = None
site = None


def initialise_site():
    """Define  global object so it can be called from anywhere."""
    global site
    site = Site()


class Site(object):
    def __init__(self):
        self.NAME = "Site de lottery - Le sombréro argentée"
        self.VERSION = "0.1"
        #
        # Configuration file
        self.conf_file = siteConfiguration("le_sombrero_argentee.conf")


class siteConfiguration(object):

    def __init__(self, configuration_file):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(configuration_file)

    def get_site_debug(self):
        return self.config.get("app", "debug")

    def get_site_port(self):
        return self.config.get("app", "port")

    def get_site_i_host(self):
        return self.config.get("i", "host")

    def get_site_i_port(self):
        return self.config.get("i", "port")

    def get_site_i_service(self):
        return self.config.get("i", "service")

    def get_site_p_host(self):
        return self.config.get("p", "host")

    def get_site_p_port(self):
        return self.config.get("p", "port")

    def get_site_p_service(self):
        return self.config.get("p", "service")

