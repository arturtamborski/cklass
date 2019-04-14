import re

from cklass import load_config


class Config:
    """ Configuration values and settings.
    Uppercase variables are global - merged from envvars and config files.
    Lowercase variables are private.
    """

    # Path to hiera repo
    HIERA_DIR = 'default value for hiera'

    # Directory name where this script will pull haproxy repos
    HAPROXY_DIR = 'default value for haproxy'

    # Output in JSON format?
    JSON = False

    class Alpha:
        XD = 'default value for xd'
        class Beta:
            class Gamma:
                PARAM = ''


    # private variables, not overwritten by config files
    server_pattern = re.compile(
        r'^\s+server\s+' +
        r'(?P<server>[\w-]+)' +
        r'\s+(?P<host>[\w-]+)' +
        r':(?P<port>\d+)',
        re.MULTILINE)

    backend_pattern = re.compile(
        r'^\s+server\s+' +
        r'(?P<server>[\w-]+)' +
        r'\s+(?P<host>[\w-]+)' +
        r':(?P<port>\d+)',
        re.MULTILINE)

    repository_name_pattern = re.compile(
        r'(?P<dc>[\w\.]+)' +
        r'-haproxy' +
        r'(?P<number>[\d]*-[\d]*)')


    # Meta
    _type_safe = True
    #_env_var_prefix = 'HASIOK'
    _config_filepath = ['~', '.']
    _secret_filepath = ['~', '.']
    _config_filename = 'config.yaml'
    _secret_filename = 'secret.yaml'


load_config(Config)

print(f'''HIERA_DIR = {Config.HIERA_DIR}
HAPROXY_DIR = {Config.HAPROXY_DIR}
JSON = {Config.JSON}
Alpha:
    XD = {Config.Alpha.XD}
    Beta:
        Gamma:
            PARAM = {Config.Alpha.Beta.Gamma.PARAM}''')
