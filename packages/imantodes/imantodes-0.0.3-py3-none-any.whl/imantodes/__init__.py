# imantodes: lightweight Python code for making interactive scivis apps
# Copyright © 2025. University of Chicago
# SPDX-License-Identifier: LGPL-3.0-only

# __init__.py: for initializing the `imantodes` package

## below is one way to set __version__ automatically, but it leaves cruft
## learned via (GLK's) https://chatgpt.com/c/684d00a8-1f58-8010-87e3-ae6501b8c991
# from importlib.metadata import version, PackageNotFoundError
#
# try:
#    __version__ = version('imantodes')
# except PackageNotFoundError:
#    __version__ = '0.0.0'  # fallback during local dev or testing

__version__ = '0.0.3'   # see also ../../pyproject.toml

# https://docs.python.org/3/tutorial/modules.html

# Vec2, Vec3, Vec4, Mat2, Mat3, Mat4, VecMatParseAction
from . import vecmat

# parm_spec_freeze, create_cli_parm_parser, create_incr_cli_parm_parser,
# get_parsed_cli_parms, list_calc_funcs,
# Changed, DepNode, DepGraph, AppState, Widgetish,
from . import app

# EventType, Event, convert
from . import event

# all the submodules within, for "from imantodes import *"
__all__ = ['vecmat', 'app', 'event']
