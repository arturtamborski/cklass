## cklass

**Hierarchical config loader from files and env variables to class.**

This module takes care of loading configuration files, secret files 
and environment variables to single configuration class without a hassle!


### Features:

- easy to use (just one function!) and configure
- comes with sane defaults
- logical hierarchical order of importance
- supports infinite number of file formats via custom format loaders
- automatic lookup of config and secret files in specified directories


### Constraints:

- all keys are case-insensitive


### Installation
```bash
pip install cklass
```

### Usage

All you have to do is to create a class and call function
`cklass.load_config()` with it as an argument.


#### Case Sensitivity

Class name (and nested classes which represent dictionaries)
have to be upper-cased or title-cased, eg. `Config` or `CONFIG`
will work, but `config` won't.

All variables that you want to search and match have to be upper-cased.
This also means that all keys are **not** case sensitive.

For example:
```yaml
# config.yaml
login:    'this will be ignored'
password: 'this will be ignored'

uSER:
    logIN: 'pi'
    paSSwoRD: 'raspberry'
```
```yaml
# secret.yaml
User:
    # this will overwrite `logIN` and `pasSSwoRD` from above
    login: 'root' 
    password: 'yrrebpsar'
```
```bash
# env variable
EXPORT USER__PASSWORD='mytopsecretpassword'
```
```python
# python
import cklass 

class User:
    LOGIN = 'this string will be overwritten'
    password = 'this will NOT be overwritten'
    Password = 'this will NOT be overwritten'
    PASSWORD = 'default password, will be overwritten'
    
    other_variable_kinda_like_private = 42

cklass.load_config(User)
``` 
    

#### Hierarchy

Every class-level keys have to be nested in top-level dictionary named
same as the class. Only class attributes will be overwritten,
there is _no_ possibility to add new attributes only by defining
them in configuration files.

Each class loaded by `cklass.load_config()` will have it's attributes
overwritten according to order specified below:

1. All values defined in class code are considered as default
2. Function will look for first config file with filename defined in 
`_config_filename` and found in `_config_filepath` list of dirs 
will be taken into account and overwrite the values set in (1).
3. Function will look for first secret file with filename defined in 
`_secret_filename` and found in `_secret_filepath` list of dirs 
will be taken into account and overwrite the values set in (1) and (2).
4. Function will look for matching environment variables of type `str`
with optional prefix defined in `_environ_prefix` and overwrite the values
set in (1), (2) and (3).


```python
# python
import cklass

# any name will work
class Config:

    PATH_TO_SOMETHING = '/etc/default/path/'
    
    class User:
        NAME  = ''
        EMAIL = ''
        PASS  = ''

    DEBUG = False

    class SERVER:
      OPEN_PORTS = ['80']

    SECRET_KEY = ''
    
    _type_safe = True
    _environ_prefix = 'MYAPP'
    _config_filename = 'config.yaml'
    _secret_filename = 'secret.json'
    _config_filepath = ['/etc/myapp/conf/']
    _secret_filepath = ['.']
    _format_loaders  = {
        'json': ['jsonlib',  'read'],
        'yaml': ['metayaml', 'read'],
    }


cklass.load_config(Config)
```
```yaml
# config.yaml
config:
    path-to-something: /etc/app/
    debug: True

    server:
      open-ports:
        - '22'
        - '80'
        - '443'
```
```yaml
# secret.yaml
config:
    user:
        name: Your Secret Name
        email: example@example.com
```
```bash
# envvars.sh
export MYAPP__CONFIG__SECRET_KEY="supersecretkey"
export MYAPP__CONFIG__USER__PASS="secretpassword"
```


#### Default Values

Every class passed to `cklass.load_config()` can define below variables with appropriate
type for some manipulating it's behaviour.

All values specified below are considered as default. Any of these variables can be omitted.


##### Type Safety

```python
_type_safe = True
```
This will compare and ensure that all keys overwritten in config/secret file have the same
type as the variables defined in class except `None`. If set to `False` this check 
will be skipped.
Example:  
`Config.VALIDATE_ME = True` will match only `bool` type from config file.  
`Config.DOESNT_MATTER = None` will match any type from config file and environment variable
`CONFIG__DOESNT_MATTER`.


##### Environment Prefix

```python
_environ_prefix = ''
```
This allows you to define custom environment variable prefix to act as a namespace.
You could for example set this to `'MYAPP'` which would cause to look up only
environment variables starting with such prefix, like `MYAPP__CONFIG__HOME_DIR`.
Class and nesting is defined with two underscores `__`, hence key names may contain
only single underscores - eg. `CORRECT_NAME`, `INCORRECT___NAME`.

Environment variables support three types: bool converted from string `TRUE` / `FALSE`,
numbers converted from string with numbers and string if two previous conversions failed.


##### Config / Secret File Names

```python
_config_filename = 'config.yaml'
_secret_filename = 'secret.yaml'
```
File name of the config. Extension has to match the defined one in `_format_loaders`.
    
    
##### Config / Secret File Paths

```python
_config_filepath = ['.']
_secret_filepath = ['.']
```
List of paths where function will look for `_config__filename` and `_secret_filename`.
For example, You could change it to `['~', '.']` which would cause the function to 
search for `config.yaml` in `$HOME/config.yaml` and then in `$PWD/config.yaml`.
Only the first file which will be successfully opened will be taken into account.


##### Format Loaders
```python
_format_loaders  = {
    'ini':  ['ini',  'load'],
    'json': ['json', 'load'],
    'toml': ['toml', 'load'],
    'yaml': ['yaml', 'safe_load'],
}
```

Format loaders consists of a nested dictionary with key matching file extension
and value defined as a two-element list. Default format loader enables the usage
of `ini`, `json`, `toml` and `yaml` file types.
In order for this to work you need to have installed appropriate python packages
specified in the list.  
Example: `yaml: ['metayaml', 'read']` says that for any config/secret file
with `yaml` extension will be loaded via `read` function defined in `metayaml` module.


#### Real-Live Example

See [examples](https://github.com/arturtamborski/cklass/tree/master/examples) directory.

```python
# config.py
import cklass

class Root:
    _environ_prefix = 'SIMPLEWEBAPP'
    _config_filepath = ['./conf']
    _secret_filepath = ['./conf']

class Common(Root):
    NAME = 'Simple Web App'
    DEBUG = True
    DATE = ''
    
    BASE_DIR = '/app'
    SRC_DIR = './src'
    
    ALLOWED_HOSTS = []
    
    class Secret:
        KEY = ''
    
    _config_filename = 'common.yaml'
    _secret_filename = 'common.json'

class Database(Root):
    ENGINE = 'sqlite3'
    HOST = 'localhost'
    NAME = 'simplewebapp_db'
    PORT = 1111
    
    class Credentials:
        USER = 'readonly'
        PASS = 'readonly'
    
    _config_filename = 'database.yaml'
    _secret_filename = 'database.json'
    
cklass.load_config(Common)
cklass.load_config(Database)


print(f'''
Common:
    NAME = '{Common.NAME}'
    DEBUG = {Common.DEBUG}
    DATE = '{Common.DATE}'

    BASE_DIR = '{Common.BASE_DIR}'
    SRC_DIR = '.{Common.SRC_DIR}'

    ALLOWED_HOSTS = {Common.ALLOWED_HOSTS}

    Secret:
        KEY = '{Common.Secret.KEY}'


Database:
    ENGINE = '{Database.ENGINE}'
    HOST = '{Database.HOST}'
    NAME = '{Database.NAME}'
    PORT = {Database.PORT}

    Credentials:
        USER = {Database.Credentials.USER}'
        PASS = '{Database.Credentials.PASS}'
''')
``` 
```yaml
# conf/common.yaml 
Common:
  debug: no
  allowed-hosts:
    - 'localhost'
    - '127.0.0.1'
    - 'mydomain.local'
```
```json
# conf/common.json
{
  "Common": {
    "Secret": {
      "key": "AAAAAAAA"
    }
  }
} 
``` 
```yaml
# conf/database.yaml
Database:
  engine: postgresql
  host: psql://localhost
``` 
```json
# conf/database.json
{
  "database": {
    "credentials": {
      "user": "dbuser",
      "pass": "pbpass"
    }
  }
} 
``` 
```bash
# conf/environment.sh
#!/bin/bash

export SIMPLEWEBAPP__COMMON__DEBUG=TRUE
export SIMPLEWEBAPP__COMMON__DATE="$(date)"
export SIMPLEWEBAPP__COMMON__SECRET__KEY="seckey"

export SIMPLEWEBAPP__DATABASE__PORT=6621
export SIMPLEWEBAPP__DATABASE__CREDENTIALS__PASS="supersecretdbpass"
```
    
##### Result
```bash
source conf/environment.sh
python3 config.py
```
```python
Common:
    NAME = 'Simple Web App'
    
    # overwritten in conf/common.yaml
    # then overwritten by environment variable
    DEBUG = True
    
    # overwritten by environment variable
    DATE = 'Mon Apr 15 12:35:39 CEST 2019'
    
    BASE_DIR = '/app'
    SRC_DIR = './src'
    
    # overwritten in conf/common.yaml
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mydomain.local']
    
    class Secret:
        # overwritten in conf/common.json
        # then overwritten by environment variable
        KEY = 'seckey'

Database:
    # overwritten in conf/database.yaml
    ENGINE = 'postgresql'
    HOST = 'psql://localhost'
    NAME = 'simplewebapp_db'

    # overwritten by environment variable
    PORT = 6621
    
    class Credentials:
        # overwritten in conf/database.json
        USER = 'dbuser'
        
        # overwritten in conf/database.json
        # then overwritten by environment variable
        PASS = 'supersecretdbpass'
```
