from http.server import HTTPServer, BaseHTTPRequestHandler
import gzip
import requests
import os
import shutil
import pandas
import json
import ipaddress


class IPtoASN(HTTPServer):
    def __init__(self, host='localhost', port=8080, DB_DIR='./', DB_FNAME='ip2asn.tsv.gz'):
        self.dirDB = DB_DIR
        self.fnameDB = DB_FNAME
        self.updateDB()
        self.loadDB()
        super().__init__((host, port), self.RequestHandler)

    def updateDB(self):
        URL = "https://iptoasn.com/data/ip2asn-combined.tsv.gz"
        try:
            r = requests.get(URL, stream=True)
        except Exception:
            raise
        if r.status_code == 200:
            with open(os.path.join(self.dirDB, self.fnameDB), 'wb') as fDL:
                shutil.copyfileobj(r.raw, fDL)

    def loadDB(self):
        with gzip.open(os.path.join(self.dirDB, self.fnameDB), 'r') as fDB:
            header = ["range_start", "range_end", "AS_number", "country_code", "AS_description"]
            self.db = pandas.read_csv(fDB, sep='\t', names=header)
        self.db['uint_range_start'] = self.db['range_start'].apply(lambda x: int(ipaddress.ip_address(x)))
        self.db['uint_range_end'] = self.db['range_end'].apply(lambda x: int(ipaddress.ip_address(x)))

    def queryIP(self, IP):
        uintIP = int(ipaddress.ip_address(IP))  # noqa: F841
        queryStr = "uint_range_start <= @uintIP <= uint_range_end"
        return self.db.query(queryStr)

    class RequestHandler(BaseHTTPRequestHandler):
        def sendJson(self, j, status=200):
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(j).encode('utf-8'))

        def do_GET(self):
            args = self.path.split('/')
            if args[1] == 'api' and args[2] == 'ip':
                row = self.server.queryIP(args[3]).to_dict(orient='records')[0]
                if row:
                    j = {
                        'ip': args[3],
                        'as_number': row['AS_number'],
                        'as_country_code': row['country_code'],
                        'as_description': row['AS_description'],
                        'range_start': row['range_start'],
                        'range_end': row['range_end']
                    }
                    self.sendJson(j, status=200)
                else:
                    j = {
                        "status": "error",
                        "message": "Could not resolve IP to ASN."
                    }
                    self.sendJson(j, status=400)
            else:
                j = {
                    "status": "error",
                    "message": "Could not understand the request.",
                    "solution": "Use path /api/ip/<IP> to query the service."
                }
                self.sendJson(j, status=400)
