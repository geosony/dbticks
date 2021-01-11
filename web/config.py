import configparser
import os

""" All configuration for the package lies here"""

config = configparser.ConfigParser()

config.read("config.ini")

#default configuration data

default_settings = {}

default_settings["log_path"] = config["default"]["api_log_path"]
default_settings["tornado_log"] = config["default"]["tornado_log"]
default_settings["web_port"] = config["default"]["web_port"]
default_settings["app_mode"] = config["default"]["app_mode"]

db_settings = {}

platform = config["env"]["platform"]

db_settings['mongo_host'] = os.environ.get("MONGO_HOST") if platform == "docker" else config["mongo"]["host"]
db_settings['mongo_port'] = int(os.environ.get("MONGO_PORT")) if platform == "docker" else config["mongo"]["port"]
db_settings['mongo_db'] = config['mongo']['db']
db_settings['mongo_pswd'] = config['mongo']['pass']

print(db_settings)