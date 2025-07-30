# -*- coding: utf-8 -*-
import warnings

warnings.warn(
    "The Arkindex API client no longer depends on APIStar. "
    "Please update your `apistar` imports to use the `arkindex` package.",
    FutureWarning,
    stacklevel=2,
)
