import hashlib
from pathlib import Path

class Monitor:
    def __init__(self, config):
        self.config = config

        # General section
        self.verbose = self.get_config_value(config, "General", "verbose")
        self.output_file = self.get_config_value(config, "General", "output_file")
        self.notification_email = self.get_config_value(config, "General", "notification_email")

        # Monitoring section
        self.target_paths = self.get_config_value(config, "Monitoring", "target_paths")
        self.target_file = self.get_config_value(config, "Monitoring", "target_file")
        self.ignored_files = self.get_config_value(config, "Monitoring", "ignored_files")
        self.ignored_dirs = self.get_config_value(config, "Monitoring", "ignored_dirs")
        self.allowed_extensions = self.get_config_value(config, "Monitoring", "allowed_extensions")
        self.blocked_extensions = self.get_config_value(config, "Monitoring", "blocked_extensions")

        # Checksum section
        self.checksum_algorithm = self.get_config_value(config, "Checksum", "checksum_algorithm")

    def start(self):
        if not self.target_paths and not self.target_file:
            print("'target_paths' / 'target_file' not set - nixShield has nothing to monitor!")
            return

        if self.allowed_extensions and self.blocked_extensions:
            print("Don't whitelist and blacklist at the same time - Check 'allowed_extensions' and 'blocked_extensions'")
            return

        if self.checksum_algorithm not in ["sha256", "md5"]:
            print("Only these algorithms are currently supported: 'sha256' / 'md5'")
            return

        if not self.output_file:
            print("'output_file' not set!")
            return
        self.output_file = Path(self.output_file).expanduser()
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.output_file.touch(exist_ok=True)

        if self.verbose:
            pass  # turn on verbose logging stuff

        if self.notification_email:
            pass  # will send messages to mail - this will be coded later

    def get_sha256sum(self, file_path, buff_size=64 * 1024):
        alg = hashlib.new(self.checksum_algorithm)
        buffer = bytearray(buff_size)
        buffer_view = memoryview(buffer)

        with open(file_path, "rb", buffering=0) as f:
            while True:
                chunk = f.readinto(buffer_view)
                if not chunk:
                    break
                alg.update(buffer_view[:chunk])
            return alg.hexdigest()

    @staticmethod
    def get_config_value(config, section, option, default=None):
        if config.has_option(section, option):
            return config.get(section, option)
        return default

    @staticmethod
    def parse_list_values(value):
        return [item.strip() for item in value.split("\n") if item.strip()]

    @staticmethod
    def validate_path(path):
        pass
