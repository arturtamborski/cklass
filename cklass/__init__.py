import os


__author__ = 'Artur Tamborski <atamborski@egnyte.com>'
__license__ = 'MIT'
__all__ = ['load_config']


def _get_attr(klass, attr_name, default_value=None):
    value = getattr(klass, attr_name, default_value)

    if type(value) is type(default_value):
        return value

    raise TypeError("Type of '%s.%s' attribute differs from the expected "
                    "type '%s'." % (klass.__name__, attr_name,
                                    type(default_value).__name__))


def _set_attr(klass, attr_name, value, safe):
    attr = getattr(klass, attr_name)

    if not safe or attr is None or type(attr) is type(value):
        return setattr(klass, attr_name, value)

    raise TypeError("'%s.%s' expected value with type '%s', got value '%s' "
                    "with type '%s' instead." % (klass.__name__, attr_name,
                     type(attr).__name__, value, type(value).__name__))


def _deep_merge(source, destination):
    for key, value in source.items():
        if type(value) is dict:
            node = destination.setdefault(key, {})
            _deep_merge(value, node)
        else:
            if destination is None:
                destination = {}
            destination[key] = value
    return destination


def _uppercase_keys_in_dict(data):
    ret = {}

    for key, value in data.items():
        new_key = key.replace('-', '_').upper()

        if type(data[key]) is dict:
            value = _uppercase_keys_in_dict(data[key])

        ret[new_key] = value
    return ret


def _load_first_file_from_dirs(name, dirs):
    config_loaders = {
        'ini':  ['ini', 'load'],
        'json': ['json', 'load'],
        'toml': ['toml', 'load'],
        'yaml': ['yaml', 'safe_load']
    }

    for d in dirs:
        path = os.path.expanduser(d) + '/' + name
        if not os.path.isfile(path):
            continue

        with open(path) as file:
            try:
                ext = name.rsplit('.')[1]
                mod = config_loaders[ext][0]
                fun = config_loaders[ext][1]
                load_fun = getattr(__import__(mod), fun)
                data = load_fun(file)
                if data:
                    return _uppercase_keys_in_dict(data)

            except ImportError:
                raise ImportError("Failed to load '%s'. Could not "
                                  "find module that supports '%s' "
                                  "file format." % (name, ext))
    return {}


def _overwrite_attrs(klass, config, safe, env_prefix=''):
    klass_name = klass.__name__

    if env_prefix:
        env_prefix += '__'

    for attr_name in dir(klass):
        attr_value = getattr(klass, attr_name)
        sub_config = config[klass_name.upper()]

        if attr_name.islower():
            continue

        if type(attr_value) is type:
            if not attr_name.istitle():
                continue

            if sub_config[attr_name.upper()] is None:
                raise TypeError("Class '%s.%s' expected value with"
                                " type 'dict', got 'None' instead."
                                % (klass_name, attr_name))

        # we're dropping case sensitivity here
        attr_name = attr_name.upper()
        klass_name = klass_name.upper()

        if type(attr_value) is not type:
            env_name = env_prefix + klass_name + '__' + attr_name
            value = attr_value

            if attr_name in sub_config:
                value = sub_config[attr_name]

            if env_name in os.environ:
                value = os.environ[env_name]

            _set_attr(klass, attr_name, value, safe)
        else:
            _overwrite_attrs(attr_value, sub_config, safe,
                             env_prefix=env_prefix + klass_name)


def load_config(klass):
    """ Update config class with values found in configuration file,
        secrets file and environment variables.
    """
    if not isinstance(klass, type):
        raise TypeError("Function 'load_config()' expected value with "
                        "'class' type as an argument, got value with "
                        "type '%s' instead." % type(klass).__name__)

    t_safe = _get_attr(klass, '_type_safe', True)
    prefix = _get_attr(klass, '_env_var_prefix', '')
    c_name = _get_attr(klass, '_config_filename', 'config.yaml')
    s_name = _get_attr(klass, '_secret_filename', 'secret.yaml')
    c_path = _get_attr(klass, '_config_filepath', ['.'])
    s_path = _get_attr(klass, '_secret_filepath', ['.'])
    config = _load_first_file_from_dirs(c_name, c_path)
    secret = _load_first_file_from_dirs(s_name, s_path)
    config = {klass.__name__.upper(): _deep_merge(secret, config)}

    _overwrite_attrs(klass, config, t_safe, env_prefix=prefix)