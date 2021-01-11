from logger import error_logger as elog, info_logger as ilog
from config import *
import motor.motor_tornado

import tornado
from tornado.options import define, options


define("port", default=default_settings["web_port"], help="run on the given port", type=int)
define("debug", default=True, help="debug mode")

handler = default_settings['tornado_log'] 
tornado.options.options.log_file_prefix = handler
tornado.options.parse_command_line()

ilog.info("Starting db")

try:
    _mongo_host = db_settings['mongo_host'] if db_settings['mongo_host'] else 'localhost'
    _mongo_port = db_settings['mongo_port'] if db_settings['mongo_port'] else 27017

    _db = motor.motor_tornado.MotorClient(_mongo_host, _mongo_port).dbtickets

    _db_conn_sts = True
    ilog.info("[Mongo] - DB connection has established!")
except Exception as e:
    _db = None
    _db_conn_sts = False
    ilog.critical("[Mongo] - DB connection has failed - {}".format(e))
    elog.critical("[Mongo] - DB connection has failed - {}".format(e))



settings = {}
settings['debug'] = options.debug 
settings['cookie_secret'] = "dbtockets@ZhS3cr3T" 
settings['mongo_conn_sts'] = _db_conn_sts
settings['mongo'] = _db

