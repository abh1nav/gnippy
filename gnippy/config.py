# -*- coding: utf-8 -*-

try:
    import configparser as ConfigParser

except ImportError:
    import ConfigParser

import os

from gnippy.errors import ConfigFileNotFoundException, IncompleteConfigurationException


# These are all the configurable settings by setting
VALID_OPTIONS = {
    "Credentials": ('username', 'password'),
    "PowerTrack": ('url', 'rules_url')
}


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
        Parses the .gnippy file at the provided location.
        Returns a dictionary with all the possible configuration options,
        with None for the options that were not provided.
    """
    if not os.path.isfile(config_file_path):
        raise ConfigFileNotFoundException("Could not find %s" % config_file_path)

    # Attempt to parse the config file
    result = {}
    parser = ConfigParser.SafeConfigParser()
    parser.read(config_file_path)

    for section in VALID_OPTIONS:
        keys = VALID_OPTIONS[section]
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


def resolve(kwarg_dict):
    """
        Look for auth and url info in the kwargs.
        If they don't exist check for the environment variables
        GNIPPY_URL
        GNIPPY_RULES_URL
        GNIPPY_AUTH_USERNAME
        GNIPPY_AUTH_PASSWORD
        If they don't exist, look for a config file path and resolve auth & url info from it.
        If no config file path exists, try to load the config file from the default path.
        If this method returns without errors, the dictionary is guaranteed to contain:
        {
            "auth": ("username", "password"),
            "url": "PowerTrackUrl"
        }
    """
    conf = {}
    if "auth" in kwarg_dict:
        conf['auth'] = kwarg_dict['auth']
    else:
        username = os.getenv("GNIPPY_AUTH_USERNAME")
        password = os.getenv("GNIPPY_AUTH_PASSWORD")

        if username and password:
            conf['auth'] = (username, password)

    if "url" in kwarg_dict:
        conf['url'] = kwarg_dict['url']
    elif os.getenv("GNIPPY_URL"):
        conf['url'] = os.getenv("GNIPPY_URL")

    if 'rules_url' in kwarg_dict:
        conf['rules_url'] = kwarg_dict['rules_url']
    elif os.getenv('GNIPPY_RULES_URL'):
        conf['rules_url'] = os.getenv("GNIPPY_RULES_URL")

    if "auth" not in conf or ("url" not in conf and 'rules_url' not in conf):

        if "config_file_path" in kwarg_dict:
            file_conf = get_config(config_file_path=kwarg_dict['config_file_path'])

        else:
            file_conf = get_config(config_file_path=get_default_config_file_path())

        if "auth" not in conf:
            creds = file_conf['Credentials']
            if creds['username'] and creds['password']:
                conf['auth'] = (creds['username'], creds['password'])
            else:
                raise IncompleteConfigurationException(
                    "Incomplete authentication information provided. "
                    "Please provide a username and password.")

        if "url" not in conf and file_conf['PowerTrack']['url']:
            # Not raising an exception on missing url, because user may
            # only want to manage rules, so streaming url is optional.
            conf['url'] = file_conf['PowerTrack']['url']

        if "rules_url" not in conf and file_conf['PowerTrack']['rules_url']:
            # Not raising an exception on missing rules_url, because user may
            # only want to consume streaming data with PowerTrack client,
            # so rules_url is optional.
            conf['rules_url'] = file_conf['PowerTrack']['rules_url']

        if 'url' not in conf and 'rules_url' not in conf:
            raise IncompleteConfigurationException("Please provide a PowerTrack url or rules_url.")

    return conf
