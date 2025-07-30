### IMPORTS
### ============================================================================
## Standard Library
import argparse
import inspect
import logging
import logging.handlers
from pathlib import Path
import sys
import warnings

# Note: Can only stop using Union / Option in py310+
from typing import Any, Dict, List, Union, Optional, Type, IO


import __main__

## Installed
import colorlog
import dataclassy

## Application
from .config import ConfigLoader
from .logging import LoggingMixin, get_log_level, logging_file_handler_errors_kwargs


### CLASSES
### ============================================================================
@dataclassy.dataclass(slots=True)  # pylint: disable=unexpected-keyword-arg
class LoggingManifest:
    """Simplified configuration of an `Application`'s logging.

    Warning: Important:
        Be careful when modifying these options. Errors during logging setup may
        cause the application to error before any logging is setup causing errors
        to not be sent to the log files (making debugging much harder). The
        initial logging will use settings from both the console and file logging
        settings.

    Attributes:
        default_level: Default logging level. Actual log level will be computed
            from this level and the application's verbosity args.
        additional_namespaces: Additional namespaces that should be logged.
        initial_log_location: Directory for storing the initial log
        initial_log_filename: filename of the initial log. Will be formatted
            with the application's name.
        initial_log_level: logging level of initial log.
        console_stream: stream to output console logging to
        console_format: text format for console logging
        console_format_style: console_format format style
        console_date_format: console_format date format
        file_enabled: enable logging to files.
        file_default_location: default log file location. Actual location
            may be changed from the applications log-dir arg.
        file_filename: filename of log. Will be formatted with the applications
            name.
        file_format: text format for file logging
        file_format_style: file_format format style
        file_date_format: file_format date format
        file_max_size: max size of a log file in bytes (see `RotatingFileHandler`).
        file_backup_count: number of old log files to keep (see `RotatingFileHandler`).
    """

    # pylint: disable=too-few-public-methods,too-many-instance-attributes

    # General
    default_level: int = logging.INFO
    additional_namespaces: List[str] = dataclassy.factory(list)
    # Literal require py38
    # log_format: Literal["text", "json"] = "text"
    # log_format: str = "text"

    # Initial Logging
    initial_log_location: str = "/var/tmp"
    initial_log_filename: str = "{name}.init.log"
    initial_log_level: Union[str, int] = logging.INFO

    # Console / Stream Logging
    console_stream: IO = sys.stderr
    console_format: str = "[{asctime}][{log_color}{levelname}{reset}]: {message}"
    console_format_style: str = "{"
    console_date_format: str = "%H:%M:%S"

    # File Logging
    file_enabled: bool = True
    file_default_location: str = "/var/tmp"
    file_filename: str = "{name}.log"
    file_format: str = "[{asctime}][{process}][{name}][{levelname}]: {message}"
    file_format_style: str = "{"
    file_date_format: str = "%Y%m%dT%H%M%S%z"
    file_max_size: int = 10 * 2**20
    file_backup_count: int = 5


class Application(LoggingMixin):
    """Base class for running applications.

    Child classes should override the `self.main` method with their application logic.

    Some attributes should be set on the class while others will be computed and
    set on the instance. All attributes that are set on the class have default
    value and are optional. They are tagged as `(class)` below.

    **Important**: the types in the Attributes table below represent the type
    on the instance, some of these (e.g. `name`) shadow the ones set on the class
    (on purpose).

    Attributes:
        name: (class) name of application - used in logging.
        application_name: (class) argparse prog name.
        epilog: (class) argparse help text epilog (e.g. copyright info).
        version: (class) version of application - used in argparse help text.
        logging_manifest: (class) configuration of application's logging.
        config_args_enabled: (class) enable collecting config from args.
        config_required: (class) providing a config file or directory via args is mandatory.
        default_config: (class) default config of the application
        config_loader_class: (class) ConfigLoader to use with the application.
        logger: logger of application
        log_level: computed logging level
        args: parsed arguments from argparse
        config_loader: the ConfigLoader of the application.
        config: the config_loader.config dict.
    """

    name: Optional[str] = None
    application_name: Optional[str] = None
    epilog: Optional[str] = None
    version: Optional[str] = None

    logging_manifest: LoggingManifest = LoggingManifest()

    config_args_enabled: bool = True
    config_required: bool = False
    default_config: Dict[str, Any] = {}
    config_loader_class: Type[ConfigLoader] = ConfigLoader

    def __init__(self, argv: Optional[List[str]] = None):
        """
        Args:
            argv: arguments to pass to this application. If `None` will collect from
                `sys.argv` instead.
        """
        # Note: we do the bare minimum of setup during __init__. This is so that
        # - we can inspect / modify the application before any state-change has occured
        # - we can ensure that any code that might fail is run after logging has been
        #   setup (this may be the critical or general loggers)
        self.name: str = self._get_name()
        self.application_name: str = self._get_application_name()

        self._argv: List[str] = argv if argv is not None else sys.argv[1:]
        self._setup_called: bool = False

        self.logger: logging.Logger = logging.getLogger(self.name)
        self._logging: argparse.Namespace = argparse.Namespace()

        # attributes populated during init
        self.log_level: int
        self.config_loader: ConfigLoader
        self.config: Dict[str, Any]
        self._arg_parser: argparse.ArgumentParser
        self.args: argparse.Namespace

        # TODO: warn if config_args_enabled = False and config_required = True
        return

    def setup(self, *, suppress_warning: bool = False) -> None:
        """Prepare the application to be run

        In no particular order, this will:

        - Setup Logging
        - Parse arguments
        - Load configuration

        Once called the following instance attributes will be populated:

        - `self.args`
        - `self.config`
        - `self.config_loader`
        - `self.log_level`

        Generally you will not need to call this method as it is called during `self.run`.

        This method may only be called once per an instance. If it is called multiple
        times, subsequent calls will have no effect and a `RuntimeWarning` will be emited.

        If this method is overridden in a child class, it should call `super().setup()` or
        otherwise set `self._setup_called` to `True` to indicate the the application has
        been correctly setup.

        Args:
            suppress_warning: Suppress the `RuntimeWarning` if this method is called multiple times.
        """
        if self._setup_called:
            if not suppress_warning:
                warnings.warn(RuntimeWarning("Attempted to call init multiple times"), stacklevel=2)
            return
        self._setup_called = True

        ## Initial Logging
        self._setup_initial_logging()

        ## Setup Config Loader
        self.config_loader = self.config_loader_class(default_config=self.default_config)
        self.config = self.config_loader.config

        ## Parse Aguments
        self._arg_parser = self.get_argument_parser()
        self.args = self._arg_parser.parse_args(self._argv)

        # Argument checks that can't be done in the parser:
        if (
            self.config_args_enabled
            and self.config_required
            and not self.args.config_dirs
            and not self.args.config_paths
        ):
            self._arg_parser.error("Must provide config via --config or --config-dir")

        ## Load Config
        if self.config_args_enabled:
            for path in self.args.config_dirs:
                self.config_loader.load_config_directory(path)
            for path in self.args.config_paths:
                self.config_loader.load_config(path)

        # Setup Logging
        self._setup_logging()
        return

    def run(self, *, prevent_exit: bool = False) -> int:  # pylint: disable=too-many-branches
        """Run this application until completion.

        Args:
            prevent_exit: Do not call `sys.exit` and instead allow the method to return.

        Returns:
            the exit_code that would have been passed to `sys.exit`
        """
        exit_code: Optional[int] = None

        ## Setup
        try:
            self.setup()
        except SystemExit as e:
            if isinstance(e.code, str) or e.code is None:
                exit_code = 254
            else:
                exit_code = e.code
        except Exception as e:  # pylint: disable=broad-except
            self.critical(
                f"Uncaught Exception in setup!\ne: {e}\nargv: {self._argv}", exc_info=True
            )
            exit_code = 255

        if exit_code is not None:
            if not prevent_exit:
                sys.exit(exit_code)
            return exit_code

        # Check that setup called correctly
        if not self._setup_called:
            warnings.warn(
                RuntimeWarning(
                    "Application setup has been completed but `_setup_called` is not `True`. This may be because you have incorrectly overridden application setup. If you have overridden setup and believe you have correctly done so without calling `super().setup()` then you can suppress this warning by setting `_setup_called=True` during the custom setup method."
                )
            )

        ## Main
        try:
            exit_code = self.main()
        except SystemExit as e:
            if isinstance(e.code, str) or e.code is None:
                exit_code = 252
            else:
                exit_code = e.code
        except KeyboardInterrupt:
            self.warning("Received KeyboardInterrupt. Shutting down...")
            exit_code = 250
        except Exception as e:  # pylint: disable=broad-except
            self.critical(f"Uncaught Exception in main!\nargv: {self._argv}", exc_info=True)
            exit_code = 253

        exit_code = exit_code if exit_code is not None else 0
        if not prevent_exit:
            sys.exit(exit_code)
        return exit_code

    def main(self) -> Optional[int]:
        """Main application entrypoint.

        Child classes MUST implement this method.

        Returns:
            An integer exit code. `None` will be converted to `0` during application exit.
        """
        raise NotImplementedError("main method not implemented")

    def get_argument_parser(self) -> argparse.ArgumentParser:
        """Get the argument parser for this application.

        To add your own arguments you should override this method and call `super().get_argument_parser()`.
        """
        ## Create Parser
        parser_kwargs: Dict[str, Any] = {
            "prog": self.application_name,
            "epilog": self.epilog,
            "description": (
                inspect.cleandoc(self.__class__.__doc__) if self.__class__.__doc__ else None
            ),
            "formatter_class": argparse.RawDescriptionHelpFormatter,
        }

        # Actually create parser
        parser = argparse.ArgumentParser(**parser_kwargs)

        ## Add Arguments
        if self.config_args_enabled:
            # Note: as config can be passed through multiple arguments, config_required is checked
            # during setup to avoid forcing users to pass a config file and a config directory.
            parser.add_argument(
                "-c",
                "--config",
                action="append",
                metavar="CONFIG_PATH",
                dest="config_paths",
                required=False,
                default=[],
                help="Add a config file to parse. Config files are parsed in the order they are added with values being merged into the previously parsed config.",
            )
            parser.add_argument(
                "--config-dir",
                action="append",
                metavar="CONFIG_DIRECTORY",
                dest="config_dirs",
                required=False,
                default=[],
                help="Add a directory to parse config files from. Directories are parsed before config files and are parsed in the order they are added. Files within the directory are added in alphabetical/lexical order.",
            )

        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Increase logging verbosity",
        )

        if self.logging_manifest.file_enabled:
            parser.add_argument(
                "--log-dir",
                metavar="PATH",
                default=self.logging_manifest.file_default_location,
                help=f"Set where log files should be stored. Defaults to {self.logging_manifest.file_default_location}",
            )

        if self.version is not None:
            parser.add_argument("--version", action="version", version=self.version)

        return parser

    def _get_name(self) -> str:
        if self.__class__.name is not None:
            return self.__class__.name

        if self.__class__.__module__ == "__main__":
            if __main__.__spec__ is None:
                # Not a package, use current filename
                return Path(sys.argv[0]).stem
            module_name = __main__.__spec__.name
        else:
            module_name = self.__class__.__module__
        return module_name.split(".", 1)[0]

    def _get_application_name(self) -> str:
        if self.__class__.application_name is not None:
            return self.__class__.application_name

        # Note: in the future and for py310+ we could use sys.orig_argv

        if self.__class__.__module__ == "__main__":
            if __main__.__spec__ is None:
                # Not a package use script name
                return Path(sys.argv[0]).name
            module_name = __main__.__spec__.name
        else:
            module_name = self.__class__.__module__

        executable = Path(sys.executable).name

        return f"{executable} -m {module_name}"

    def _setup_initial_logging(self):
        ## Console Logging
        console_handler = logging.StreamHandler(self.logging_manifest.console_stream)
        console_handler.setLevel(self.logging_manifest.initial_log_level)

        console_formatter = colorlog.ColoredFormatter(
            self.logging_manifest.console_format,
            datefmt=self.logging_manifest.console_date_format,
            reset=False,
            log_colors={
                "VVDEBUG": "purple",
                "VDEBUG": "purple",
                "DEBUG": "purple",
                "INFO": "bold_blue",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_white,bg_red",
            },
            style=self.logging_manifest.console_format_style,
            stream=self.logging_manifest.console_stream,
        )

        console_handler.setFormatter(console_formatter)
        self._logging.console_handler = console_handler

        self.logger.addHandler(console_handler)

        ## Initial File Logging
        if self.logging_manifest.file_enabled:
            initial_handler = (
                logging.handlers.RotatingFileHandler(  # pylint: disable=unexpected-keyword-arg
                    Path(self.logging_manifest.initial_log_location)
                    / self.logging_manifest.initial_log_filename.format(name=self.name),
                    encoding="utf8",
                    **logging_file_handler_errors_kwargs("replace"),
                )
            )
            initial_handler.setLevel(self.logging_manifest.initial_log_level)

            file_formatter = logging.Formatter(
                self.logging_manifest.file_format,
                datefmt=self.logging_manifest.file_date_format,
                style=self.logging_manifest.file_format_style,
            )
            self._logging.file_formatter = file_formatter

            initial_handler.setFormatter(file_formatter)
            self._logging.initial_handler = initial_handler

            self.logger.addHandler(initial_handler)
        return

    def _setup_logging(self):
        log_level = get_log_level(self.args.verbose, self.logging_manifest.default_level)
        self.log_level = log_level

        ## File Logging
        if self.logging_manifest.file_enabled:
            file_handler = (
                logging.handlers.RotatingFileHandler(  # pylint: disable=unexpected-keyword-arg
                    Path(self.args.log_dir)
                    / self.logging_manifest.file_filename.format(name=self.name),
                    encoding="utf8",
                    **logging_file_handler_errors_kwargs("replace"),
                )
            )
            file_handler.setLevel(log_level)

            file_handler.setFormatter(self._logging.file_formatter)
            self._logging.file_handler = file_handler

        ## Update Console Logging
        self._logging.console_handler.setLevel(log_level)

        ## Update self.logger
        self.logger.setLevel(log_level)
        if self.logging_manifest.file_enabled:
            self.logger.addHandler(file_handler)
            self.logger.removeHandler(self._logging.initial_handler)

        ## Additional logging namespaces
        for namespace in self.logging_manifest.additional_namespaces:
            logger = logging.getLogger(namespace)
            logger.setLevel(log_level)
            logger.addHandler(self._logging.console_handler)
            if self.logging_manifest.file_enabled:
                logger.addHandler(file_handler)
        return
