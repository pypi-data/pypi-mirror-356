import logging
import inspect
from executing import Source
from .kFormatter import kColorFormatter, kNoColorFormatter

class kLogger:

    def __init__(self, tag, logfile=None, loglevel="DEBUG"):
        if not loglevel:
            loglevel = "DEBUG"
        self.tag = tag 
        self.logfile = logfile
        self.loglevel = loglevel
        self.logger = logging.getLogger(self.tag)
        self.logger.setLevel(self.loglevel.upper())

        if not self.logfile:
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(kColorFormatter())
        else:
            self.ch = logging.FileHandler(self.logfile)
            self.ch.setFormatter(kNoColorFormatter())
        self.ch.setLevel(self.loglevel.upper())

        if not self.logger.handlers:
            self.logger.addHandler(self.ch)

    def __call__(self, *args):
        if args:
            for arg in args:
                callFrame = inspect.currentframe().f_back
                callNode = Source.executing(callFrame).node
                source = Source.for_frame(callFrame)
                expression = source.asttokens().get_text(callNode.args[0])
                self.logger.info(f'{expression} | {arg}', stacklevel=2)
        else:
            self.logger.info("", stacklevel=2)

    def debug(self, message):
        self.logger.debug(message, stacklevel=2)

    def info(self, message):
        self.logger.info(message, stacklevel=2)

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        self.logger.error(message, stacklevel=2)

    def critical(self, message):
        self.logger.critical(message, stacklevel=2, stack_info=True)

    def setLevel(self, level):
        self.loglevel = level.upper()
        self.logger.setLevel(level.upper())
        self.ch.setLevel(level.upper())

    def setFile(self, file):
        self.logfile = file
        if file:
            self.logger.handlers.clear()
            self.logger.setLevel(self.loglevel.upper())

            self.ch = logging.FileHandler(self.logfile)
            self.ch.setFormatter(kNoColorFormatter())
            self.ch.setLevel(self.loglevel.upper())
            self.logger.addHandler(self.ch)

    def addFile(self, file):
        ch = logging.FileHandler(file)
        ch.setFormatter(kNoColorFormatter())
        ch.setLevel(self.loglevel.upper())
        self.logger.addHandler(ch)
        
def get_logger(tag, logfile, loglevel):
    return kLogger(tag, logfile, loglevel)
