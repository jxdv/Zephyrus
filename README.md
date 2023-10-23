# Zephyrus

> File integrity monitoring (FIM) is an internal control or process that performs the act of validating the integrity of
operating system and application software files using a verification method between the current file state and a known,
good baseline. This comparison method often involves calculating a known cryptographic checksum of the file's original
baseline and comparing with the calculated checksum of the current state of the file. 
Other file attributes can also be used to monitor integrity.

## Installation

```commandline
git clone https://github.com/jxd1337/Zephyrus.git
cd Zephyrus/
python3 -m venv env && source env/bin/activate
(env) pip3 install -r requirements.txt
```

Run tests:

```commandline
python3 -m unittest core/tests/test_sum.py
```

## Usage

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

### CLI examples

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

## Interactive interface

```commandline
 ______          _                          
|___  /         | |                         
   / / ___ _ __ | |__  _   _ _ __ _   _ ___ 
  / / / _ \ '_ \| '_ \| | | | '__| | | / __|
 / /_|  __/ |_) | | | | |_| | |  | |_| \__ \
/_____\___| .__/|_| |_|\__, |_|   \__,_|___/
          | |           __/ |               
          |_|          |___/                
    
Enter 'help' or '?' to see all available commands

zephyrus> ?
help / ? - show this help message
config - show current config
load - load baseline
start - start monitoring
email - configure notifications to be sent out using mail
exit - exit Zephyrus
```

Most of these commands are pretty self-explanatory.

'config' example output:

```commandline
zephyrus> config
This is the current Zephyrus config. Restart with different CLI args to change it.
--------------------------------------------------
[+] Number of Targets: 1001
[+] Monitoring interval: 21600s
[+] Hashing algorithm: md5
[+] Verbosity: True
[+] Ignored prefixes: ['_lae', 'test_']
[+] Ignored suffixes: ['.ll', '.o']
--------------------------------------------------
```

'load' example output (with verbose logging):

```commandline
...
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file787.bin'): da2af396ffcb39261ebe7c03e2923426
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file260.bin'): aa5ab1b0a645186430e70fd6cd88cc81
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file152.bin'): 60f803cb32657ecfdf95018295ce1003
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file610.bin'): 3a3d3fa8392a97ca9740559b1d554f12
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file114.bin'): 7410be02622df8e5e13f5e03ac9b2d36
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file781.bin'): 5ed4de09bbe98351810f2df17e02a0a3
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file061.bin'): 556ffbf4d210ac0374639f8aaf65d78e
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file997.bin'): ac3d3c65c0215f5549f1c184f0fcd3b0
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file741.bin'): b3a8bb638e6d152ae8463c28e9ac8d2f
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file714.bin'): 9e5ac14e60e9158946662c7a92468ea2
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file030.bin'): a16320d6335a26ee0696daad106d4858
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file004.bin'): a57d02ee0057397b56143c5fc91642dd
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file219.bin'): 4417fc08bbe1d18acf5e3f3d3fc2bc1d
core.monitor > INFO > Writing Target('/home/jxd/Desktop/test_data/file023.bin'): 6e056f433cfd1becd212c23453c35785
core.monitor > INFO > Baseline loaded.
```

'start' example output (with detected changes):

```commandline
zephyrus> start
core.monitor > INFO > Monitoring..
core.monitor > WARNING > /home/jxd/Desktop/test_data/file123.bin checksum doesn't match!
core.monitor > WARNING > /home/jxd/Desktop/test_data/file667.bin checksum doesn't match!
core.monitor > WARNING > /home/jxd/Desktop/test_data/file500.bin checksum doesn't match!
```

### Verification & Caching of changed targets

Zephyrus uses LevelDB to store the target and its corresponding hash as a key, value.
Once the verify_baseline function is called, We calculate checksum of each target and call verify_target_integrity.

For the sake of simplicity and non-redundancy we cache all targets which have modified checksums to avoid spamming of
warnings. It could be especially annoying if we have configured email notifications and lower interval.

```python
def verify_baseline(self):
    for target in self.targets:
        target_checksum = target.checksum()
        verified = self.verify_target_integrity(str(target), target_checksum)
        if not verified and str(target) not in self.cache:
            self.cache.append(str(target))
            logger.warning(f"{target} checksum doesn't match!")
            
def verify_target_integrity(self, target_path, target_checksum):
    sn = self.db.snapshot()
    stored_checksum = sn.get(target_path.encode())

    return stored_checksum.decode() == target_checksum
```

## TODO

- Email configuration -> as of right now gmail requires phone number in order to create a new account, and as a person
who values his privacy I'll need to find a way to bypass this or maybe use another mail provider.

## Contributing

Zephyrus is in very early version. Any contributions are welcome!

## License

[GPL](LICENSE)