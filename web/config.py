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
db_settings['mongo_user'] = os.environ.get("MONGO_USER") if platform == "docker" else config["mongo"]["user"]
db_settings['mongo_pswd'] = os.environ.get("MONGO_PSWD") if platform == "docker" else config["mongo"]["pass"]
db_settings['mongo_connect_params'] = os.environ.get("MONGO_CONNECT_PARAMS") if platform == "docker" else config["mongo"]["connect_params"]
db_settings['mongo_uri_connect'] = os.environ.get("MONGO_URI_CONNECT") if platform == "docker" else config["mongo"]["conn_uri"]

print(db_settings)