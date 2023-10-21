import sys
import os

from .target import Target
from .db import LevelStorage
from .log import ZephyrusLogger
from .utils import zephyrus_prompt

logger = ZephyrusLogger(__name__)


class Monitor:
    def __init__(self, target, hash_alg, verbose, threads, ignored_prefixes, ignored_suffixes):
        self.target_dir = target
        self.hash_alg = hash_alg
        self.verbose = verbose
        self.threads = threads
        self.ignored_prefixes = ignored_prefixes
        self.ignored_suffixes = ignored_suffixes
        self.targets = []

    @staticmethod
    def help_cmd():
        print("help / ? -> show this help message")
        print("email -> configure notifications to be sent out using mail")
        print("load -> load / reload baseline")
        print("exit -> exit Zephyrus and stop monitoring")

    def parse_target_dir(self, target):
        if not os.path.isdir(target):
            logger.info(f"{target} is not a directory!")
            sys.exit(1)

        for path, _, files in os.walk(target):
            for name in files:
                file_path = os.path.join(path, name)
                if not self.filter_check(name):
                    target = Target(file_path, self.hash_alg)
                    self.targets.append(target)

        if not self.targets:
            logger.info("Target directory is empty!")
            sys.exit(1)

    def filter_check(self, file_path):
        if self.ignored_prefixes:
            return any(file_path.startswith(prefix) for prefix in self.ignored_prefixes)
        if self.ignored_suffixes:
            return any(file_path.endswith(suffix) for suffix in self.ignored_suffixes)
        return False

    def load_baseline(self):
        db = LevelStorage()
        db.write_batch(self.targets)

    def email_config(self):
        pass

    def menu(self):
        print("""
Current Zephyrus monitoring configuration is below. If you'd like to change any of these settings,
terminate Zephyrus and run again with correct CLI args.
        """)
        print("-" * 50)
        print(f"[+] Number of Targets: {len(self.targets)}")
        print(f"[+] Hashing algorithm: {self.hash_alg}")
        print(f"[+] Verbosity: {self.verbose}")
        print(f"[+] Number of threads: {self.threads}")
        print(f"[+] Ignored prefixes: {self.ignored_prefixes}")
        print(f"[+] Ignored suffixes: {self.ignored_suffixes}")
        print("-" * 50)

        print("Enter 'help' or '?' to see all available commands")
        while True:
            cmd = zephyrus_prompt("", choices=["help", "?", "load", "email", "exit"])

            if cmd in ["help", "?"]:
                self.help_cmd()
            elif cmd == "load":
                self.load_baseline()
            elif cmd == "email":
                self.email_config()
            elif cmd == "exit":
                logger.info("Take care!")
                sys.exit(0)

    def run(self):
        self.parse_target_dir(self.target_dir)
        self.menu()
