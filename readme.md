# cklass
### Python module for loading config from files and env variables to class

## Installation

    pip install cklass

## Usage

    # config.yaml
    path-to-something: /home/something/here
    verbose: True

    server:
      open_ports:
        - '22'
        - '80'
        - '443'


    # secret.yaml
    user-name: Your Name
    email-address: example@example.com


    # envvars.sh
    export CONFIG__SECRET_KEY="asdasdasd"


    # config.py
    import cklass

    class Config:
        PATH_TO_SOMETHING = ''

        USER_NAME = ''
        EMAIL_ADDRESS = ''

        MY_VARIABLE = True
        VERBOSE = False

        class Server:
          OPEN_PORTS = []

        SECRET_KEY = ''
        
        # Default settings
        _type_safe = True
        _env_var_prefix = ''
        _config_filepath = ['~', '.']
        _secret_filepath = ['~', '.']
        _config_filename = 'config.yaml'
        _secret_filename = 'secret.yaml'


    cklass.load_config(Config)
