import tornado
from logger import error_logger as elog, info_logger as ilog
from handlers.core import Core
from handlers.similarity import Similarity
from handlers.logParser import Logparser
from bson.objectid import ObjectId
from datetime import datetime

class UploadHandler(Core, Logparser):


    async def post(self):
        """ 'Add New Ticket'
        
        Post:
           title: Ticket title 
           ...

        Exceptions:
            MissingArgumentError: if any of the mandatory arguments are missing

        Error Codes:
            ...

        Returns:
            response(json): json response 
    
        """
        self._handler = "upload"
        postData = {}
        postData["title"] = self.get_argument("title")
        postData["jiraID"] = self.get_argument("jiraID")

        dateStr = self.get_argument("date")
        postData["date"] = self.getMongoDate(dateStr)
        postData["dateStr"] = self.getParsedDateFormat(dateStr, "%Y-%m-%d")

        postData["status"] = self.get_argument("status")
        postData["module"] = self.get_argument("module")
        postData["team"] = self.get_argument("team")

        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]

                with open("uploads/" + filename, 'wb') as fp:
                    fp.write(body)

                ilog.info('POST "{}" "{}" {} bytes'.format(filename, content_type, len(body)))


        qp = self.parse(filename)

        if not qp:
            self._res_code = "UPLOAD_PARSE_EMPTY_02"
            payload = [{"msg": "Upload file parsed an empty result"}]
        else:
            now = datetime.now()
            for p in qp:

                doc = {"about": postData, "log": p, "last_updated_on": now}
                result = await self.db.slow_queries.insert_one(doc)
                ilog.info("{}".format(result.inserted_id))

            payload = [{"msg": "OK"}]

        self._res_code = "UPLOAD_01"
        self.send_response(payload)


class ListHandler(Core):


    async def get(self):
        """ 'List Tickets'
        
        Params:
           title: Ticket title 
           ...

        Exceptions:
            MissingArgumentError: if any of the mandatory arguments are missing

        Error Codes:
            ...

        Returns:
            response(json): json response 
    
        """
        self._handler = "tickets"

        f = self.request.arguments
        mongo_filter = {}

        for key, v in f.items():
            val = self.decode_argument(v[0])

            if key == 'jid':
                _v = {"$regex": val + ".*" }
                mongo_filter["about.jiraID"] = _v
            elif key == "fdt":
                fdstr = self.getMongoDate(val)
                _v = {"$gte": fdstr}
                mongo_filter["about.date"] = _v
            elif key == "tdt":
                _v = self.getMongoDate(val)
                if "$gte" in mongo_filter["about.date"]:
                    mongo_filter["about.date"]["$lte"] = _v
                else:
                    mongo_filter["about.date"] = {"$lte": _v }
            elif key == "sts":
                mongo_filter["about.status"] = val


        payload = []
        i = 1

        async for doc in self.db.slow_queries.find(mongo_filter, {"about"}):

            about = doc["about"]
            p = {
                    "sino": i,
                    "_id": str(doc["_id"]),
                    "date":  self.getParsedDateFormat(about["dateStr"], "%d %b, %Y"),
                    "jiraID": about["jiraID"],
                    "title": about["title"],
                    "module": about["module"],
                    "team": about["team"],
                    "state": about["status"],
                }

            payload.append(p)
            i += 1


        self._res_code = "LIST_01"
        self.send_response(payload)



class TicketDetailHandler(Core):


    async def get(self, _id):
        """ 'Get Detail of a Ticket'
        
        Params:
           _id: Ticket ID in mongo
           ...

        Exceptions:
            MissingArgumentError: if any of the mandatory arguments are missing

        Error Codes:
            ...

        Returns:
            response(json): json response 
    
        """
        self._handler = "detail"

        payload = []

        doc = await self.db.slow_queries.find_one({"_id": ObjectId(_id)}, {"about", "log"})

        if "date" in doc["about"]:
            doc["about"].pop("date", None)

        p = { 
                "ticket": doc["about"], 
                "datetime": doc["log"]["reported"] if "reported" in doc["log"] else {"date": "", "time": ""}, 
                "host": doc["log"]["host"] if "host" in doc["log"] else {"host": "", "ip": ""}, 
                "db": doc["log"]["db"] if "db" in doc["log"] else "", 
                "analytics": doc["log"]["analytics"], 
                "query": doc["log"]["query"]["def"], 
                "querytitle": doc["log"]["query"]["title"] if "title" in doc["log"]["query"] else "",
                "queryfix": doc["log"]["query"]["fix"] if "fix" in doc["log"]["query"] else "",
            }

        payload.append(p)

        self._res_code = "DETAIL_01"
        self.send_response(payload)

class TicketUpdateHandler(Core):

    async def post(self, _id):

        self._handler = "update"
        data = tornado.escape.json_decode(self.request.body)
        now = datetime.now()

        r = await self.db.slow_queries.update_one({"_id": ObjectId(_id)}, 
                {"$set" : 
                    {
                        "log.query.title": data["qtitle"],
                        "log.query.fix": data["qfix"],
                        "about.jiraID": data["jiraID"],
                        "about.title": data["title"],
                        "about.date": self.getMongoDate(data["repDate"]),
                        "about.dateStr": self.getParsedDateFormat(data["repDate"], "%Y-%m-%d"),
                        "about.status": data["status"],
                        "about.team": data["team"],
                        "about.module": data["module"],
                        "last_updated_on": now
                    }
                })

        payload = []

        if r is not True:
            self._res_code = "UPDATE_00"

        self._res_code = "UPDATE_01"
        self.send_response(payload)


class TicketCompareHandler(Core, Similarity):


    async def get(self, _id):
        """ 'Compare Ticket
        
        Params:
           _id: Ticket ID in mongo
           ...

        Exceptions:
            MissingArgumentError: if any of the mandatory arguments are missing

        Error Codes:
            ...

        Returns:
            response(json): json response 
    
        """
        self._handler = "compare"
        payload = []

        doc = await self.db.slow_queries.find_one({"_id": ObjectId(_id)}, {"log.query.min"})
        qm = doc["log"]["query"]["min"]
        
        async for odoc in self.db.slow_queries.find({}, {"log.query.min", "about.jiraID"}):
            oqm = odoc["log"]["query"]["min"]
        
        
            if str(odoc["_id"]) != _id:
        
                s = self.calcSimilarity(qm, oqm)
                if round(s*100) > 40:
                    payload.append({"_id": str(odoc["_id"]), "jiraID": odoc["about"]["jiraID"], "sim": round(s*100, 2)})


        if payload:
            payload = sorted(payload, key = lambda i: i["sim"], reverse=True)
        
        self._res_code = "COMPARE_01"
        self.send_response(payload)
