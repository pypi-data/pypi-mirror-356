### IMPORTS
### ============================================================================
## Standard Library
import logging
import sys
from typing import Dict, Type

import __main__

## Installed

## Application


## CONSTANTS
### ============================================================================
VDEBUG = 8
VVDEBUG = 6

### SETUP
### ============================================================================
# Create extra logging levels
for level, level_name in ((VDEBUG, "VDEBUG"), (VVDEBUG, "VVDEBUG")):
    # Note: it would be more efficient to use logging.getLevelNamesMapping but
    # requires py311
    current_level_name = logging.getLevelName(level)
    if not current_level_name.startswith("Level ") and current_level_name != level_name:
        # TODO: raise warning about overriding name?
        pass
    # always set the level name even if we raised a warning
    logging.addLevelName(level, level_name)

del level, level_name, current_level_name


### FUNCTIONS
### ============================================================================
def get_log_level(verbosity: int, default_level: int) -> int:
    """Get the log level based on the default log level.

    This function essentially adds a "verbosity level" per "major log level" lower than
    the default.

    For example, if `default_level == DEBUG`, then `verbosity == 1` will return `VDEBUG` and
    `verbosity >= 2` will return `VVDBEUG`. For any `defaul_level > INFO` will always use
    4 levels of verbosity (`INFO`, `DEBUG`, `VDEBUG`, `VVDEBUG`).
    """
    # pylint: disable=too-many-return-statements,too-many-branches

    if default_level <= VVDEBUG:
        return default_level

    if default_level <= VDEBUG:
        if verbosity > 0:
            return VVDEBUG
        return default_level

    if default_level <= logging.DEBUG:
        if verbosity >= 2:
            return VVDEBUG
        if verbosity == 1:
            return VDEBUG
        return default_level

    if default_level <= logging.INFO:
        if verbosity >= 3:
            return VVDEBUG
        if verbosity == 2:
            return VDEBUG
        if verbosity == 1:
            return logging.DEBUG
        return default_level

    if verbosity >= 4:
        return VVDEBUG
    if verbosity == 3:
        return VDEBUG
    if verbosity == 2:
        return logging.DEBUG
    if verbosity == 1:
        return logging.INFO
    return default_level


def logging_file_handler_errors_kwargs(errors: str) -> Dict[str, str]:
    """Generate FileHandler keyword argument if it is supported by this python version.

    If it is not supported contains an empty dictionary.

    To use it unpack it like so `FileHandler(**logging_file_handler_errors_kwargs())`
    """
    if sys.version_info >= (3, 9):
        return {"errors": errors}
    return {}


def get_logger_name_for_instance(instance: object, prefix: str = "") -> str:
    """Get a logger name based on the qualified name of this instance's class.

    Args:
        instance: object to inspect
        prefix: optional prefix for the logger name.
    """
    return get_logger_name_for_class(instance.__class__, prefix)


def get_logger_name_for_class(cls: Type[object], prefix: str = "") -> str:
    """Get a logger name based on the qualified name of a class.

    Args:
        cls: object to inspect
        prefix: optional prefix for the logger name.
    """
    if cls.__module__ == "__main__":
        module_name = __main__.__spec__.name if __main__.__spec__ is not None else "__main__"
    else:
        module_name = cls.__module__
    logger_name = f"{module_name}.{cls.__qualname__}"

    if prefix:
        return f"{prefix}.{logger_name}"

    return logger_name


### CLASSES
### ============================================================================
class LoggingMixinBase:  # pylint: disable=too-few-public-methods
    """Base class for logging mixins"""

    logger: logging.Logger

    @classmethod
    def get_logger(cls, prefix: str = "") -> logging.Logger:
        """Get a `logging.Logger` for this class

        Args:
            prefix: optional prefix for the logger name
        """
        return logging.getLogger(get_logger_name_for_class(cls, prefix))


class LoggingMixin(LoggingMixinBase):
    """Adds shortcut logging methods to a class

    Expects that a `logging.Logger` exists at `self.logger`
    """

    logger: logging.Logger

    def vvdebug(self, msg: str, *args, **kwargs) -> None:
        """Log a Very Verbose Debug (VVDEBUG) message.

        When you're tired of finding the bug and want to log everything.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self.logger.log(VVDEBUG, msg, *args, **kwargs)
        return

    def vdebug(self, msg: str, *args, **kwargs) -> None:
        """Log a Verbose Debug (VDEBUG) message.

        More than debug, less than everything.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self.logger.log(VDEBUG, msg, *args, **kwargs)
        return

    def debug(self, msg: str, *args, **kwargs) -> None:
        """Log a DEBUG message

        Basic debug messages
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self.logger.debug(msg, *args, **kwargs)
        return

    def info(self, msg: str, *args, **kwargs) -> None:
        """Log an INFO message

        Print something to the screen/logfile so we know what is happening
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self.logger.info(msg, *args, **kwargs)
        return

    def warning(self, msg: str, *args, **kwargs) -> None:
        """Log a WARNING message

        Something is wrong but we likely can recover or skip it without issue.

        In a larger system this will likely just go to centralised logging.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self.logger.warning(msg, *args, **kwargs)
        return

    def error(self, msg: str, *args, **kwargs) -> None:
        """Log an ERROR message

        Something bad has happened but we caught it. We might be able to continue,
        but other things might start breaking. We can probably still safely exit.

        In a larger system, this will likely cause a gentle alert to be placed somewhere.
        An end user might receive a useful error message (like a HTTP 4xx 5xx).
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self.logger.error(msg, *args, **kwargs)
        return

    def critical(self, msg: str, *args, **kwargs) -> None:
        """Log a CRITICAL message

        Something is on fire. We somehow caught it but we probably need to exit now.
        If we keep going more things may catch on fire.

        In a larger system, someone is probably going to get paged over this.
        An end user is definitely going to get an error message, probably not even
        a useful one, just a HTTP 500.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self.logger.critical(msg, *args, **kwargs)
        return


class UnderscoreLoggingMixin(LoggingMixinBase):  # pylint: disable=too-few-public-methods
    """Add shortcut logging methods to a class with underscore (`_`) prefix

    Expects that a `logging.Logger` exists at `self._logger`.
    """

    _logger: logging.Logger

    def _vvdebug(self, msg: str, *args, **kwargs) -> None:
        """Log a Very Verbose Debug (VVDEBUG) message.

        When you're tired of finding the bug and want to log everything.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self._logger.log(VVDEBUG, msg, *args, **kwargs)
        return

    def _vdebug(self, msg: str, *args, **kwargs) -> None:
        """Log a Verbose Debug (VDEBUG) message.

        More than debug, less than everything.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self._logger.log(VDEBUG, msg, *args, **kwargs)
        return

    def _debug(self, msg: str, *args, **kwargs) -> None:
        """Log a DEBUG message

        Basic debug messages
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self._logger.debug(msg, *args, **kwargs)
        return

    def _info(self, msg: str, *args, **kwargs) -> None:
        """Log an INFO message

        Print something to the screen/logfile so we know what is happening
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self._logger.info(msg, *args, **kwargs)
        return

    def _warning(self, msg: str, *args, **kwargs) -> None:
        """Log a WARNING message

        Something is wrong but we likely can recover or skip it without issue.

        In a larger system this will likely just go to centralised logging.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self._logger.warning(msg, *args, **kwargs)
        return

    def _error(self, msg: str, *args, **kwargs) -> None:
        """Log an ERROR message

        Something bad has happened but we caught it. We might be able to continue,
        but other things might start breaking. We can probably still safely exit.

        In a larger system, this will likely cause a gentle alert to be placed somewhere.
        An end user might receive a useful error message (like a HTTP 4xx 5xx).
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self._logger.error(msg, *args, **kwargs)
        return

    def _critical(self, msg: str, *args, **kwargs) -> None:
        """Log a CRITICAL message

        Something is on fire. We somehow caught it but we probably need to exit now.
        If we keep going more things may catch on fire.

        In a larger system, someone is probably going to get paged over this.
        An end user is definitely going to get an error message, probably not even
        a useful one, just a HTTP 500.
        """
        if "stacklevel" not in kwargs:
            kwargs["stacklevel"] = 2
        self._logger.critical(msg, *args, **kwargs)
        return


class NotFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Ignore the given logger (and all subloggers).

    Is the opposite of `logging.Filter`.

    References:
        - https://docs.python.org/3/library/logging.html#filter-objects
    """

    def __init__(self, name: str) -> None:
        # pylint: disable=super-init-not-called

        if not name:
            # An empty string would cause all records to be ignored.
            raise ValueError("name cannot be empty string")

        self._filter = logging.Filter(name)
        return

    def filter(self, record) -> bool:
        "As per `logging.Filter.filter`"
        return not self._filter.filter(record)
