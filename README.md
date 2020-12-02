![](docs/ip2asn.png)

Python3 HTTP API for resolving IP addresses to their ASN. The resolving API can be useful in pentesting or incident response/threat analysis. Best used locally. Usage as a production server is not advised. Internally utilizes the database downloaded from https://iptoasn.com.

# Usage

After running the server like in `example.py`, it will download the latest ASN database from https://iptoasn.com.   
Once the database is received, indices are created to easily search the dataset later. This may take a moment.
```bash
$ python3 example.py
ASN-Database loaded. Starting API..
```

To query ASN information about an IP simply query the `/api/ip/<IP>` path, e.g.:

```bash
$ curl localhost:8080/api/ip/1.1.1.1
{"ip": "1.1.1.1", "as_number": 13335, "as_country_code": "US", "as_description": "CLOUDFLARENET - Cloudflare, Inc.", "range_start": "1.1.1.0", "range_end": "1.1.1.255"}
```

That's all!

The server returns a `json` with keys:
| Key | Type |
|---|---|
| ip | String | 
| as_number | Number | 
| as_country_code | String | 
| as_description | String | 
| range_start | String | 
| range_end | String | 



# Docker

The image is available on https://hub.docker.com/chmey/ip2asn.

I recommend using the Docker image over a local instance.

Spinning it up is as simple as:
```bash
$ sudo docker run --rm -p 8080:8080 chmey/iptoasn
```

# Contributions
Contributions are welcome. Please respect the BSD 2 LICENSE.
