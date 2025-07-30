import logging

class kFormatter(logging.Formatter):
    grey = "\x1b[34;20m"
    blue = "\x1b[38;20m"
    yellow = "\x1b[36;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[41;1m"
    reset = "\x1b[0m"
    format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"


class kColorFormatter(kFormatter):
    #format dictionary
    FORMATS = {
        logging.DEBUG: kFormatter.grey + kFormatter.format + kFormatter.reset,
        logging.INFO: kFormatter.blue + kFormatter.format + kFormatter.reset,
        logging.WARNING: kFormatter.yellow + kFormatter.format + kFormatter.reset,
        logging.ERROR: kFormatter.red + kFormatter.format + kFormatter.reset,
        logging.CRITICAL: kFormatter.bold_red + kFormatter.format + kFormatter.reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class kNoColorFormatter(kFormatter):
    #format dictionary
    FORMATS = {
        logging.DEBUG: kFormatter.format,
        logging.INFO: kFormatter.format,
        logging.WARNING: kFormatter.format,
        logging.ERROR: kFormatter.format,
        logging.CRITICAL: kFormatter.format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

