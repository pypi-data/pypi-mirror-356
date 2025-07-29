import sys
import logging
import traceback
from _jcpy import find_class


LOG_LEVEL_TO_LOGENTRY_MAP = {
    logging.FATAL: "CRITICAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARN",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "UNSPECIFIED",
    -float("inf"): "DEBUG",
    15: "NOTICE",
    5: "TRACE",
}


def _map_log_level(level: int) -> str:
    try:
        return LOG_LEVEL_TO_LOGENTRY_MAP[level]
    except KeyError:
        return max(
            java_level
            for python_level, java_level in LOG_LEVEL_TO_LOGENTRY_MAP.items()
            if python_level <= level
        )


class PythonLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        try:
            PythonLogWriter = find_class("jcpy.engine.PythonLogWriter")
            self._logger_writer = PythonLogWriter()
        except Exception as e:
            logging.getLogger(__name__).error(
                "Failed to initialize PythonLogWriter: %s", e
            )
            raise

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        name = f"{record.module}:{record.lineno or 'unknown'}"
        trace = None
        if record.exc_info:
            trace = "".join(traceback.format_exception(*record.exc_info))
        severity = _map_log_level(record.levelno)
        self._logger_writer.log(name, severity, message, trace)


class LoggingPrint:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, msg):
        if msg.strip():
            self.logger.log(self.level, msg.rstrip())

    def flush(self):
        pass


# Configure logger
logger = logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
python_log_handler = PythonLogHandler()
logger.addHandler(python_log_handler)

# Redirect stdout and stderr to logger
# sys.stdout = LoggingPrint(logger, logging.INFO)
# sys.stderr = LoggingPrint(logger, logging.ERROR)
