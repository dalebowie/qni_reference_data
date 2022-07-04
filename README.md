# QNI Reference Data

This repository contains a series of python scripts that can be used to populate reference data in a QRadar deployment with one or more QRadar Network Insights hosts. 

Currently, this repository hosts the following:
* ja3er_to_qradar.py - obtains TLS JA3 hashes from [ja3er.com](https://ja3er.com), performs some filtering, and then posts to a QRadar Reference Map


## Usage

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

If you wish to re-run the script to download a fresh database of hashes, remove the local file `ja3er.json` that stores a copy of the last-downloaded database.


## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)