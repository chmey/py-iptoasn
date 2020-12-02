from http.server import HTTPServer, BaseHTTPRequestHandler
import gzip
import requests
import os
import shutil
import pandas
import ipaddress


class IPtoASN(HTTPServer, BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def __init__(self, DB_DIR='./', DB_FNAME='ip2asn.tsv.gz'):
        self.dirDB = DB_DIR
        self.fnameDB = DB_FNAME
        self.updateDB()
        self.loadDB()
        print(self.queryIP("1.1.1.1"))
        super().__init__(('localhost', 8080), self)

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
