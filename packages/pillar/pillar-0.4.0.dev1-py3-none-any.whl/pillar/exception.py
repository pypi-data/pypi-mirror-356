### IMPORTS
### ============================================================================
## Standard Library

## Installed

## Application


### CLASSES
### ============================================================================
## Generic / Shared Exceptions
## -----------------------------------------------------------------------------
class MissingDependencyError(Exception):
    """Exception for when an optional dependency is required but not installed"""

    def __init__(
        self,
        feature: str,
        required_package: str,
        package_name: str,
        optional_dependency: str,
    ) -> None:
        """
        Args:
            feature: Name of the feature. This could be a word, phrase, or longer sentence.
            required_package: Name of the package we were trying to import. Doesn't need to be
                the actual import name, could be it's colloquial or PyPI name.
            package_name: Name of our package. Used to generate install instructions.
            optional_dependency: Name of the optional dependency that should be installed. Used
                to generate install instructions.
        """
        message = f'{feature} requires {required_package} to be installed. It can be installed through the "{package_name}[{optional_dependency}]" optional dependency'
        super().__init__(message)
        return


## Pillar Specific Exceptions
## -----------------------------------------------------------------------------
class PillarException(Exception):
    """Base class for all Pillar specific exceptions"""

    def __init__(self, *args, **kwargs) -> None:
        # Allow for multiple inheritence
        super().__init__(*args, **kwargs)
        return


class PillarMissingDependencyError(PillarException, MissingDependencyError):
    """Pillar is missing a required package."""

    def __init__(self, feature: str, required_package: str, optional_dependency: str) -> None:
        """As per `MissingDependencyError` with `package_name` set to `"pillar"`"""
        super().__init__(feature, required_package, "pillar", optional_dependency)
        return
