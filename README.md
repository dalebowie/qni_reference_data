# QNI Reference Data

This repository contains a series of python scripts that can be used to populate reference data in a QRadar deployment with one or more QRadar Network Insights hosts. 

Currently, this repository hosts the following:
* ja3er_to_qradar.py - obtains TLS JA3 hashes from [ja3er.com](https://ja3er.com), performs some filtering, and then posts to a QRadar Reference Map named `QNI : JA3er Hashes`.
* abusechsslbl_to_qradar.py - obtains the "SSLBL SSL Certificate Blacklist (SHA1 Fingerprints)" from [abuse.ch](https://abuse.ch), and then posts to a QRadar Reference Map named `QNI : Abuse.ch SSL Certificate Blocklist Hashes`.
* abusechja3bl_to_qradar.py - obtains the "JA3 Fingerprint Blacklist" from [abuse.ch](https://abuse.ch), and then posts to a QRadar Reference Map named `QNI : Abuse.ch JA3 Blocklist Hashes`.


## Usage

Usage of all of the scripts can be determined by running with the `-h` flag. 

```
$ python3 ja3er_to_qradar.py -h
```

An example execution is:
```
$ python3 ja3er_to_qradar.py --skip_verify_qradar 10.0.0.1 12345678-90ab-cdef-1234-567890abcdef
```

Once the script runs successfully, you will have a reference map in your QRadar system that you can use anywhere reference data is supported. For example, in AQL:
```
SELECT sourceip, "TLS JA3 Hash", REFERENCEMAP('QNI : JA3er Hashes', "TLS JA3 Hash") as 'Possible User Agent' FROM flows WHERE "TLS JA3 Hash" IS NOT NULL AND "Possible User Agent" IS NOT NULL GROUP BY sourceip, "TLS JA3 Hash"
```

See above for the full list of scripts and resultant reference data that gets populated in QRadar.


## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)