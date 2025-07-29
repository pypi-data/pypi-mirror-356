import atexit
import os
import sys

from loguru._logger import Core, Logger


def add_relative_path(record):
    start = os.getcwd()
    record["extra"]["relative_path"] = os.path.relpath(record["file"].path, start)


logger = Logger(
    core=Core(),
    exception=None,
    depth=1,
    record=False,
    lazy=False,
    colors=False,
    raw=False,
    capture=True,
    patchers=[add_relative_path],
    extra={},
)

atexit.register(logger.remove)

__all__ = [
    "get_logger",
    "LOG_FORMAT",
]

logger.remove()

LOGGER_SINK = {}
LOG_FORMAT = (
    "[<green>{time:MM-DD HH:mm:ss}</green>|"
    "<red>{process.name}</red>|"
    "<level>{level: <8}</level>|"
    "<cyan>{file.path}</cyan>:<cyan>{line}</cyan>:<cyan>{function}</cyan>]"
    "<level>{message}</level>"
)


def get_logger(file_name=None, clear=False, **kwargs):
    global LOGGER_SINK  # pylint: disable=global-statement,global-variable-not-assigned
    if clear:
        logger.remove()
        LOGGER_SINK.clear()
    if file_name is None:
        file_name = sys.stderr
        if "level" not in kwargs:
            kwargs["level"] = "INFO"
    if "format" not in kwargs:
        kwargs["format"] = LOG_FORMAT
    if file_name in LOGGER_SINK.values():
        # FIXME:
        # logger.debug("already registered")
        logger.debug(f"{str(file_name)} already registered")
    else:
        # if "level" not in kwargs:
        # kwargs["level"] = "DEBUG" if jam_is_debug() else "INFO"
        sink_id = logger.add(file_name, **kwargs)
        LOGGER_SINK[sink_id] = file_name
        logger.debug(f"sink_id: {sink_id:02d} ---> {str(file_name)}")
    return logger
