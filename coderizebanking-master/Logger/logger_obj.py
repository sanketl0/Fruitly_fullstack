"""
Author: Nitish Patel
Last modified: 17-02-2022
"""

import logging
import logging.handlers
import sys
import datetime
import os
from pathlib import Path

date = datetime.date.today()


class Logger:
    def __init__(self, name='BasicLogger'):
        self.name = name

        self.dev_log_dir = os.path.join(Path(__file__).parent, 'dev_log_files')
        self.user_log_dir = os.path.join(Path(__file__).parent, 'user_log_files')
        self.create_logs_directory()

        self._logger = self._setup_logger(self.name + "_user", os.path.join(self.user_log_dir, 'user-log.log'),
                                          level=logging.INFO)
        self._dev_logger = self._setup_logger(self.name + "_dev", os.path.join(self.dev_log_dir, 'dev-log.log'),
                                              level=logging.DEBUG)

    # @classmethod
    def create_logs_directory(self):

        for log_dir in (self.dev_log_dir, self.user_log_dir):
            # Create log directory if not exists
            if not os.path.exists(log_dir):
                print("Creating log folder", log_dir)
                os.mkdir(log_dir)

            # Create a gitignore file in each log folder
            gitignore_file_path = os.path.join(log_dir, ".gitignore")
            if not os.path.exists(gitignore_file_path):
                with open(gitignore_file_path, 'w') as gitignore_file:
                    gitignore_file.write("*\n!.gitignore")

    @staticmethod
    def _setup_logger(name, log_file, level=logging.INFO):
        """To setup as many loggers as you want"""

        handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight')
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger(f"{name}")
        logger.setLevel(level)
        logger.addHandler(handler)

        # if level == logging.INFO:
        #     logger.addHandler(logging.StreamHandler(sys.stdout))

        logger.debug("logging started")

        return logger

    def debug(self, msg):
        self._logger.debug(msg)
        self._dev_logger.debug(msg)

    def info(self, msg):
        self._logger.info(msg)
        self._dev_logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)
        self._dev_logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)
        self._dev_logger.error(msg)

    def critical(self, msg):
        self._logger.critical(msg)
        self._dev_logger.critical(msg)
