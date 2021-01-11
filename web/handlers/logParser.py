import re

class Logparser():

    def parse(self, filename):

        f = open('uploads/' + filename, 'r')
        ls = f.readlines()
        
        d = {
                "reported": {
                    "p" : '^s*#\s*Time:\s*(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}).*$',
                    "g" : ["_", "date", "time"]
                    },
                "host": {
                    "p" : '^\s*#\s*User@Host:\s*([a-zA-Z0-9]+)\[.+\].+\[(\d{3}(?:.\d{1,3}){3})\].*$',
                    "g" : ["_", "host", "ip"]
                    },
                "db": {
                    "p" : '^\s*use\s*([a-zA-Z0-9]+);',
                    "g" : ["_", "name"]
                    },
                "analytics": {
                    "p" : '^\s*#\s*Query_time:\s*(\d+(?:\.\d+)?)\s+Lock_time: \s*(\d+(?:\.\d+)?)\s+Rows_sent:\s*(\d+)\s+Rows_examined:\s*(\d+).*$',
                    "g" : ["_", "query_time", "lock_time", "rows_sent", "rows_examined"]
                    },
                "query": {
                    "p" : '^\s*((?:SELECT|UPDATE|DELETE|INSERT).*)$',
                    "g" : ["_", "query"]
                    }
        
            }
        
        ret = []
        case = {}
        qp = []
        sq = 0
        for l in ls:
            if sq:
                qp.append(l)
                m = re.search(";$", l.rstrip())
                if m:
                    sq = 0
                    q = " ".join(qp)
                    qp = []
                    case["query"] = self._minify_query(q)
                    ret.append(case)
                    case = {}
        
            else:
                for node, meta in d.items():
                 
                    ds = []
                    m = re.search(d[node]["p"], l)
                    g = d[node]["g"]
                    
                    if m:
                        ds = { v : m.group(i) for i, v in enumerate(g) }
                        del ds["_"]
                    
                        if node == "query":
        
                            m = re.search(";$", l.rstrip())
                            if m:
        
                                q = ds["query"]
                                case["query"] = self._minify_query(q)
                                ret.append(case)
                                case = {}
        
                            else:
                    
                                # start recording query undtil we see ;
                                sq = 1
                                qp.append(ds["query"])
        
                        else:
                            case[node] = ds
                    
        
        return ret


    def _minify_query(self, q):
        qm = re.sub(r"=\s*'[^']*'", "='xxx'", q)
        qm = re.sub(r"[\s\n]+", "", qm)
        qm = qm.lower()
        return {"def": q, "min": qm}

