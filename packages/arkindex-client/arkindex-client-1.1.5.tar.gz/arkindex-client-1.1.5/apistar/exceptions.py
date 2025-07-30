# -*- coding: utf-8 -*-
import warnings

from arkindex.exceptions import ErrorResponse

__all__ = ["ErrorResponse"]

warnings.warn(
    "The Arkindex API client no longer depends on APIStar. "
    "Please update your `apistar.exceptions` imports to use the `arkindex.exceptions` module.",
    FutureWarning,
    stacklevel=2,
)
