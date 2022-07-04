# QNI Reference Data

This repository contains a series of python scripts that can be used to populate reference data in a QRadar deployment with one or more QRadar Network Insights hosts. 

Currently, this repository hosts the following:
* ja3er_to_qradar.py - obtains TLS JA3 hashes from [ja3er.com](https://ja3er.com), performs some filtering, and then posts to a QRadar Reference Map
* abusech_to_qradar.py - obtains the "SSLBL SSL Certificate Blacklist (SHA1 Fingerprints)" from [abuse.ch](https://abuse.ch), and then posts to a QRadar Reference Map


## Usage

### ja3er_to_qradar.py

Usage of the `ja3er_to_qradar.py` script can be determined by running with the `-h` flag. 

```
$ python3 ja3er_to_qradar.py -h
```

An example execution is:
```
$ python3 ja3er_to_qradar.py --skip_verify_qradar 10.0.0.1 12345678-90ab-cdef-1234-567890abcdef
```

Once the script runs successfully, you will have a "QNI - JA3er Hashes" reference map in your QRadar system that you can use anywhere reference data is supported. For example, in AQL:
```
SELECT sourceip, "TLS JA3 Hash", REFERENCEMAP('QNI : JA3er Hashes', "TLS JA3 Hash") as 'Possible User Agent' FROM flows WHERE "TLS JA3 Hash" IS NOT NULL AND "Possible User Agent" IS NOT NULL GROUP BY sourceip, "TLS JA3 Hash"
```

### abusech_to_qradar.py

Usage of the `abusech_to_qradar.py` script can be determined by running with the `-h` flag. 

```
$ python3 abusech_to_qradar.py -h
```

An example execution is:
```
$ python3 abusech_to_qradar.py --skip_verify_qradar 10.0.0.1 12345678-90ab-cdef-1234-567890abcdef
```

Once the script runs successfully, you will have a "QNI : Abuse.ch SSL Certificate Blocklist Hashes" reference map in your QRadar system that you can use anywhere reference data is supported. For example, in AQL:
```
SELECT destinationip, "X509 Certificate Fingerprint Hash", REFERENCEMAP('QNI : Abuse.ch SSL Certificate Blocklist Hashes', "X509 Certificate Fingerprint Hash") as 'Blocklist Reason' FROM flows WHERE "X509 Certificate Fingerprint Hash" IS NOT NULL AND "Blocklist Reason" IS NOT NULL GROUP BY destinationip, "X509 Certificate Fingerprint Hash"
```


## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)