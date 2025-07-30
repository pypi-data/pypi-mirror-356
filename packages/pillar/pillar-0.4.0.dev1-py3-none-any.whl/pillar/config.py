### IMPORTS
### ============================================================================
## Standard Library
from copy import deepcopy
import json
import logging
from pathlib import Path
import traceback
from typing import Dict, Any, Optional, Union
from urllib.parse import urlparse

## Installed
import deepmerge
import yaml

try:
    import orjson

    ORJSON_AVAILABLE = True
except ImportError:
    ORJSON_AVAILABLE = False

## Application
from .logging import LoggingMixin


### CLASSES
### ============================================================================
## Config Parsers
## -----------------------------------------------------------------------------
class ConfigParser:
    """Base class for config loaders."""

    def parse_content(self, content: bytes) -> Any:
        """Parse content into usable config.

        Args:
            content: Raw content to load from
        """
        raise NotImplementedError("Must be implemented by child classes")


class JsonParser(ConfigParser):
    """Config parser for JSON

    If [`orjson`](https://pypi.org/project/orjson/) is installed will use that for parsing.
    It can be installed using `pillar[recommended]`.
    """

    def parse_content(self, content: bytes) -> Any:
        """Parse config into a usable config.

        See [pillar.config.ConfigParser.parse_content][].
        """
        if ORJSON_AVAILABLE:
            return orjson.loads(content)  # pylint: disable=no-member

        ## orjson unavailable, fallback
        # TODO: raise warning
        return json.loads(content)


class YamlParser(ConfigParser):
    """Config parser for YAML"""

    # Requires [`pyaml`](https://pypi.org/project/pyaml/) to be installed.
    # ^^ this is currently the default

    def parse_content(self, content: bytes) -> Any:
        """Parse config into a usable config.

        See [pillar.config.ConfigParser.parse_content][].
        """
        return yaml.safe_load(content)


# Set default Parsers
# ..............................................................................
DEFAULT_PARSERS: Dict[str, ConfigParser] = {
    "json": JsonParser(),
    "yaml": YamlParser(),
    "yml": YamlParser(),
}


## ConfigLoad
## -----------------------------------------------------------------------------
class ConfigLoader(LoggingMixin):
    """Load and merge multiple config files from various locations.

    Attributes:
        logger:
        merger: deepmerge merger
        parsers: loaded parses
        config: computed config
        load_stack: loaded files and their respective config before merging. Because
            dictionaries are ordered this will also be in order of loading. The only
            only exception is if the same file is loaded multiple times (don't do that).
        load_errors: errors encountered when loading files. If the same file is loaded
            multiple times, it will only have the latest error encountered.
    """

    def __init__(
        self,
        default_config: Optional[Dict[str, Any]] = None,
        default_parsers: Optional[Dict[str, ConfigParser]] = None,
    ) -> None:
        """
        Args:
            default_config: Set initial `self.config` to this.
            default_parsers: Use these parsers instead of the `DEFAULT_PARSERS`.
        """
        self.logger: logging.Logger = self.get_logger()

        self.merger: deepmerge.Merger = deepmerge.Merger(
            [(dict, ["merge"]), (list, ["override"])], ["override"], ["override"]
        )

        self.parsers: Dict[str, ConfigParser] = (
            deepcopy(default_parsers) if default_parsers is not None else deepcopy(DEFAULT_PARSERS)
        )

        # loaded config
        self.config: Dict[str, Any] = deepcopy(default_config) if default_config else {}
        self.load_stack: Dict[str, Dict[str, Any]] = {}
        self.load_errors: Dict[str, Dict[str, Any]] = {}
        return

    def load_config(self, path: Union[str, Path], *, suppress_errors: bool = False) -> None:
        """Load a given config path.

        The loaded config will be merged into `self.config`. The actual config loaded will
        also be stored in `self.load_stack[path]`. Any errors during loading will be stored
        in `self.load_errors[path]`.

        Args:
            path: Path to try load from. Can include scheme (e.g. `file://config/dev.json`)
            suppress_errors: Prevent errors from being thrown while loading the config. This
                does not affect errors being stored in `self.load_errors`.

        Raises:
            ValueError: Unsupported path scheme
        """
        if isinstance(path, Path):
            path = str(path)

        try:
            parsed = urlparse(path)
            config_type = parsed.path.rsplit(".", 1)[1]

            if parsed.scheme in {"", "file"}:
                if parsed.netloc:
                    config_path = parsed.netloc + parsed.path
                else:
                    config_path = parsed.path
                with open(config_path, "rb") as f:
                    loaded = self.parsers[config_type].parse_content(f.read())
            else:
                raise ValueError(f"Unsupported scheme {parsed.scheme!r}")

            # TODO check is in correct format
            self.load_stack[path] = loaded
            self.merger.merge(self.config, loaded)

        except Exception as e:
            self.load_errors[path] = {
                "exception": e,
                "stack_trace": traceback.format_exc(),
            }
            if suppress_errors:
                return
            raise e
        return

    def load_config_directory(
        self, path: Union[str, Path], *, suppress_errors: bool = False
    ) -> None:
        """Load all config files from a given directory

        Files are loaded in alphabetical/lexical order which can be used to ensure order. For example:

        ```
        10-first-config.yml
        20-leaving-space-for-expansion.yml
        99-last-config.yml
        ```

        All available config extensions will be loaded (see: `DEFAULT_PARSERS`). Unknown filetypes
        will be skipped.

        Args:
            path: directory to scan for config files
            suppress_errors: Prevent errors from being thrown while loading. This does not affect
                errors being stored in `self.load_errors`. This will not prevent errors being
                thrown if the path does not exist.

        Raises:
            ValueError: the path is invalid.

        *Added in 0.3*
        """
        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise ValueError(f"Cannot load from {path}")

        for child in sorted(path.iterdir()):
            if child.is_file() and child.suffix[1:] in DEFAULT_PARSERS:
                # note: child.suffix includes "." we remove it with slice
                self.load_config(child, suppress_errors=suppress_errors)
        return
