import shutil
import time
import sys
import os
from pathlib import Path

from .target import Target
from .log import ZephyrusLogger
from .utils import zephyrus_prompt

import plyvel

logger = ZephyrusLogger(__name__)


class Monitor:
    def __init__(self, monitor_dir, interval, hash_alg, verbose, threads, ignored_prefixes, ignored_suffixes):
        # initial construct
        self.monitor_dir = monitor_dir
        self.interval = interval
        self.hash_alg = hash_alg
        self.verbose = verbose
        self.threads = threads
        self.ignored_prefixes = ignored_prefixes
        self.ignored_suffixes = ignored_suffixes

        self.targets = []
        self.baseline_loaded = False

        # LevelDB
        project_path = Path(__file__).absolute().parent.parent
        db_path = project_path / "storage"

        if os.path.exists(db_path):
            shutil.rmtree(db_path)

        self.db = plyvel.DB(f"{db_path}", create_if_missing=True)

    def parse_target_dir(self, target):
        if not os.path.exists(target):
            logger.info(f"{target} doesn't exist!")
            sys.exit(1)

        if not os.path.isdir(target):
            logger.info(f"{target} is not a directory!")
            sys.exit(1)

        # Recursively parse all files of the target directory
        for path, _, files in os.walk(target):
            for name in files:
                file_path = os.path.join(path, name)
                if not self.filter_check(name):
                    target = Target(file_path, self.hash_alg)
                    self.targets.append(target)

        if not self.targets:
            logger.info("No targets loaded!")
            sys.exit(1)

    def filter_check(self, file_path):
        if self.ignored_prefixes:
            return any(file_path.startswith(prefix) for prefix in self.ignored_prefixes)
        if self.ignored_suffixes:
            return any(file_path.endswith(suffix) for suffix in self.ignored_suffixes)
        return False

    def verify_target_integrity(self, target_path, target_checksum):
        sn = self.db.snapshot()
        stored_checksum = sn.get(target_path.encode())

        return stored_checksum.decode() == target_checksum

    def verify_baseline(self):
        for target in self.targets:
            target_checksum = target.checksum()
            if not self.db.verify_target_integrity(str(target), target_checksum):
                logger.warning(f"{target} checksum doesn't match!")

    def close_storage(self):
        if not self.db.closed:
            self.db.close()
            del self.db

    # Menu and command handling

    def menu(self):
        self.parse_target_dir(self.monitor_dir)

        print("Enter 'help' or '?' to see all available commands")
        while True:
            cmd = zephyrus_prompt("", choices=["help", "?", "load", "email", "exit", "start", "config"])

            if cmd in ["help", "?"]:
                self.help_cmd()
            elif cmd == "load":
                self.load_baseline()
            elif cmd == "email":
                self.email_config()
            elif cmd == "start":
                self.start_monitor()
            elif cmd == "config":
                self.show_config()
            elif cmd == "exit":
                logger.info("Take care!")
                self.db.close_db()
                sys.exit(0)

    def load_baseline(self):
        wb = self.db.write_batch()

        for target in self.targets:
            target_checksum = target.checksum()
            if self.verbose:
                logger.info(f"Writing {target}: {target_checksum}")
            wb.put(str(target).encode(), target_checksum.encode())
        wb.write()

        self.baseline_loaded = True
        logger.info("Baseline loaded.")

    def email_config(self):
        raise NotImplementedError("TODO: email configuration")

    def start_monitor(self):
        if not self.baseline_loaded:
            logger.warning("Can't start monitoring. Baseline isn't loaded!")
            return

        logger.info("Monitoring..")

        start = time.monotonic()
        while True:
            time.sleep(float(self.interval) - ((time.monotonic() - start) % 60.0))
            self.verify_baseline()

    def show_config(self):
        print("This is the current Zephyrus config. Restart with different CLI args to change it.")
        print("-" * 50)
        print(f"[+] Number of Targets: {len(self.targets)}")
        print(f"[+] Monitoring interval: {self.interval}s")
        print(f"[+] Hashing algorithm: {self.hash_alg}")
        print(f"[+] Verbosity: {self.verbose}")
        print(f"[+] Number of threads: {self.threads}")
        print(f"[+] Ignored prefixes: {self.ignored_prefixes}")
        print(f"[+] Ignored suffixes: {self.ignored_suffixes}")
        print("-" * 50)

    def help_cmd(self):
        print("help / ? - show this help message")
        print("config - show current config")
        print("load - load / reload baseline")
        print("start - start monitoring")
        print("email - configure notifications to be sent out using mail")
        print("exit - exit Zephyrus and stop monitoring")
