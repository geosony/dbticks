from logger import error_logger as elog, report_logger as rlog
import tornado
from dateutil.parser import parse


class Core(tornado.web.RequestHandler):
    """ Some untility methods that can be used across the application

        Author:
            sony@zhservices.com
    """ 

    _handler = ""
    _res_code = ""

    _info_bag = {
            "upload": {
                "version": "1.0",
                "name": "Upload a new ticket!"
                },
            "tickets": {
                "version": "1.0",
                "name": "List all tickets with filter"
                },
            "detail": {
                "version": "1.0",
                "name": "Ticket detail for the individual query"
                },
            "update": {
                "version": "1.0",
                "name": "Update ticket"
                },
            "compare": {
                "version": "1.0",
                "name": "Compare query to get similarity in percentage, with other queries",
                }
            }

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers", "accept, content-type, x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, OPTIONS")

    def options(self, *args, **kwargs):
        pass

    @property
    def db(self):
        if not self.settings['mongo_conn_sts']:
            elog.critical("DB is not initialised!!")
            raise Exception("DB is not initialised!!")
        return self.settings['mongo']



    def send_response(self, payload=[]):

        """ send the response object back to client """

        import time
        _response = {
                "error": {
                    "status": 0
                },
                "info": {
                    "version": "",
                    "name": "",
                    "timestamp": time.time()
                },
                "auth": {},
                "payload": []
        }

        _res_status = self._get_res_status()
        _response["error"]["status"] = _res_status
        if _res_status != 1:
            _response["error"]["code"] = self._res_code

        _info = self._info_bag[self._handler]
        _response["info"].update(_info)

        """
        if _res_status != 0:
            _response["auth"].update(self._auth)
        """

        _response["payload"] = payload

        self.finish(_response)
        return True

    def _get_res_status(self):

        if self._res_code:

            res_type = self._res_code[-2:]
            return int(res_type)

        return 0
    
    def getParsedDateFormat(self, d, f):
        dt = parse(d)
        return dt.date().strftime(f)
    
    def getMongoDate(self, d):
        return parse(d)

