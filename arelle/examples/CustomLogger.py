'''
This module is an example Arelle controller in non-interactive mode

@author: Mark V Systems Limited
(c) Copyright 2011 Mark V Systems Limited, All rights reserved.
'''
from __future__ import print_function

import logging
import os
import sys
import traceback

from arelle import Cntlr
from tempfile import gettempdir


class CntlrCustomLoggingExample(Cntlr.Cntlr):
    def __init__(self):
        # no logFileName parameter to prevent default logger from starting
        super().__init__()

    def run(self):
        # Add custom log handler
        logger = logging.getLogger("arelle")
        logger.addHandler(CustomLogHandler())

        model_xbrl = self.modelManager.load(os.path.join(gettempdir(), "test.xbrl"))

        self.modelManager.validateInferDecimals = True
        self.modelManager.validateCalcLB = True
        self.modelManager.validate()

        self.modelManager.close()

        self.close()


class CustomLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.level = logging.DEBUG
        if self.get_color_support():
            fmt = "\033[32m[%(messageCode)s]\033[36m (%(filename)s:%(lineno)s)\033[0m %(message)s"
        else:
            fmt = "[%(messageCode)s] (%(filename)s:%(lineno)s) %(message)s"
        self.setFormatter(logging.Formatter(fmt))

    def emit(self, logRecord):
        # noinspection PyBroadException
        try:
            print(self.format(logRecord))
        except Exception as e:
            # Failure in logging shouldn't kill the program.
            self.handleError(logRecord)

    @staticmethod
    def get_color_support():
        """
        Returns True if the running system's terminal supports color, and False
        otherwise.
        """
        plat = sys.platform
        supported_platform = plat != 'win32' or 'ANSICON' in os.environ
        # isatty is not always implemented, #6223.
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        known_supported_env = os.environ['PYCHARM_HOSTED'] == '1'
        if (not supported_platform or not is_a_tty) and not known_supported_env:
            return False
        return True


if __name__ == "__main__":
    CntlrCustomLoggingExample().run()
