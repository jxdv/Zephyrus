import logging
import sys


class ZephyrusLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO):
        self.name = name
        self.level = level

        stdout_fmt = "%(name)s > %(levelname)s > %(message)s"
        formatter = logging.Formatter(stdout_fmt)
        stdout_logger = logging.StreamHandler(sys.stdout)
        stdout_logger.setFormatter(formatter)

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.logger.addHandler(stdout_logger)

    def info(self, msg):
        """
        Log an informational message.

        Args:
            msg (str): The message to be logged as information.
        """

        self.logger.info(msg)

    def debug(self, msg):
        """
        Log a debugging message.

        Args:
            msg (str): The message to be logged for debugging purposes.
        """
        self.logger.debug(msg)

    def warning(self, msg):
        """
        Log a warning message.

        Args:
            msg (str): The message to be logged as a warning.
        """
        self.logger.warning(msg)

    def error(self, msg):
        """
        Log an error message.

        Args:
            msg (str): The message to be logged as an error.
        """
        self.logger.error(msg)
