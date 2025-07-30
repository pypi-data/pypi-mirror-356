### IMPORTS
### ============================================================================
## Standard Library
import sys
from typing import Dict, Any

## Installed

## Application


### FUNCTIONS
### ============================================================================
def dataclass_slots_kwargs() -> Dict[str, Any]:
    """Generate dataclass slots keyword argument if it is supported by this python version.

    If it is not supported contains an empty dictionary.

    To use it unpack it like so `@dataclass(**dataclass_slots_kwargs())`
    """
    # Note: We use a function rather than a constant because pylint will get confused
    # about what the value is.
    if sys.version_info >= (3, 10):
        return {"slots": True}
    return {}
