# Zephyrus

### Installation

```commandline
git clone https://github.com/jxd1337/Zephyrus.git
cd Zephyrus/
python3 -m venv env && source env/bin/activate
(env) pip3 install -r requirements.txt
```

### Usage

```commandline
usage: Zephyrus [-h] [--version] [--dir DIR] [--seconds SECONDS] [--hash {sha256,md5}]
                [--verbose] [--threads THREADS]
                [--ignore-prefix IGNORED_PREFIXES [IGNORED_PREFIXES ...]]
                [--ignore-suffix IGNORED_SUFFIXES [IGNORED_SUFFIXES ...]]

Local-based File Integrity Monitor

options:
  -h, --help            show this help message and exit
  --version             Show Zephyrus version
  --dir DIR             Path to dir which contains file to be monitored
  --seconds SECONDS     Interval to check integrity of monitored targets (6 hours by default)
  --hash {sha256,md5}   Hashing algorithm for calculating checksums (default is sha256)
  --verbose             Verbose logging
  --ignore-prefix IGNORED_PREFIXES [IGNORED_PREFIXES ...]
                        Files with supplied prefixes will be ignored
  --ignore-suffix IGNORED_SUFFIXES [IGNORED_SUFFIXES ...]
                        Files with supplied suffixes will be ignored
```

SHA256 and MD5 are supported hash algorithms. I originally added MD5 for older machines as I thought it was less CPU
intensive, but turns out It's not always the case. This [stackoverflow discussion](https://stackoverflow.com/questions/2722943/is-calculating-an-md5-hash-less-cpu-intensive-than-sha-family-functions)
gives some greater insight & explanations.
I recommend you check it out.

#### CLI examples

- Check integrity every 5 minutes
- Use MD5 for checksums
- Ignore all files ending with *.pyc, *.docx

```commandline
./zephyrus.py --dir /path/to/dir/ --seconds 300 --hash md5 --ignore-suffix .pyc .docx
```

- Ignore all files starting with 'test_'
- Enable verbose logging

```commandline
./zephyrus.py --dir /path/to/dir --ignore-prefix test_ --verbose
```

### Interactive interface



### Contributing

Zephyrus currently has only very basic FIM functionalities.
Feel free to add or suggest new ones by opening issues / PRs!

### License

[GPL](LICENSE)