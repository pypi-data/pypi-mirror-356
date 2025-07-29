""" VMAN Programmer Constants

This file is intended to be used solely by the programmer
If you are an user do not modify this file, modify config.toml instead.
"""

import os
import pathlib

# Paths
SRC_PATH = pathlib.Path(__file__).parent.resolve()
CONFIG_PATH = os.path.join(SRC_PATH, 'config.toml')
LOGGER_CONFIG_PATH = os.path.join(SRC_PATH, 'logger_conf.json')
LOGS_PATH = os.path.join(SRC_PATH, 'vman.log')

# Return codes
SUCCESS                 = 0
USER_ERROR              = 1
OPERATIONAL_ERROR       = 2
CHILD_ERROR             = 3
NO_AUTHOR_ERROR         = 8
NO_VIDEO_MANUAL_ERROR   = 16
