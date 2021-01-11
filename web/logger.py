from loguru import logger
from config import default_settings

""" Formats """

standard_format = "'time': {time:DD MMM, YYYY  HH:mm:ss:SS Z(zz)}, 'level': {level}, 'file': {file}, 'line': {line}, 'msg': {message}"
simple_format = "{time:DD MMM, YYYY  HH:mm:ss:SS Z(zz)} - {level} - {module}  - {message}"

""" Loggers """

log_path = default_settings['log_path']

logger.add(log_path + "/report.log", filter=lambda record: record["extra"].get("name") == "report", format=standard_format, rotation="monthly")
logger.add(log_path + "/errors.log", filter=lambda record: record["extra"].get("name") == "error", format=standard_format, rotation="monthly")
logger.add(log_path + "/info.log", filter=lambda record: record["extra"].get("name") == "info", format=simple_format, rotation="monthly")

report_logger = logger.bind(name="report")
error_logger = logger.bind(name="error")
info_logger = logger.bind(name="info")
