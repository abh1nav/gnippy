# -*- coding: utf-8 -*-

import ConfigParser
import os


class ConfigNotFoundException(Exception):
    """ Raised when no .gnippy file is found. """
    pass


def get_default_config_file_path():
    """
        Returns the absolute path to the default placement of the
        config file (~/.gnippy)
    """
    # --- This section has been borrowed from boto ------------------------
    # Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
    # Copyright (c) 2011 Chris Moyer http://coredumped.org/
    # https://raw.github.com/boto/boto/develop/boto/pyami/config.py
    #
    # If running in Google App Engine there is no "user" and
    # os.path.expanduser() will fail. Attempt to detect this case and use a
    # no-op expanduser function in this case.
    try:
      os.path.expanduser('~')
      expanduser = os.path.expanduser
    except (AttributeError, ImportError):
      # This is probably running on App Engine.
      expanduser = (lambda x: x)
    # ---End borrowed section ---------------------------------------------
    return os.path.join(expanduser("~"), ".gnippy")


def get_config(config_file_path=None):
    """
        Parses the .gnippy file at the provided location. If no location
        was provided, the default path is checked.
    """
    if config_file_path is None:
        config_file_path = get_default_config_file_path()

    if not os.path.isfile(config_file_path):
        raise ConfigNotFoundException("Could not find %s" % config_file_path)

    # Attempt to parse the config file
    result = {}
    parser = ConfigParser.SafeConfigParser()
    parser.read(config_file_path)

    # These are all the configurable settings by setting
    options = {
        "Credentials": ('username', 'password'),
        "PowerTrack": ("url", )
    }

    for section in options:
        keys = options[section]
        values = {}
        for key in keys:
            try:
                values[key] = parser.get(section, key)
            except ConfigParser.NoOptionError:
                values[key] = None
            except ConfigParser.NoSectionError:
                values[key] = None

        result[section] = values

    return result
