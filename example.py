from iptoasn import IPtoASN
server = IPtoASN(host='', port=8080)  # Listen on *:8080
print("ASN-Database loaded. Starting API..")
server.serve_forever()
