import logging
import sys


class ZephyrusLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO):
        self.name = name
        self.level = level
        self.format = "%(name)s > %(levelname)s > %(message)s"

        self.stdout_fmt = logging.Formatter(self.format)
        self.stdout_logger = logging.StreamHandler(sys.stdout)
        self.stdout_logger.setFormatter(self.stdout_fmt)

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.stdout_logger)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
