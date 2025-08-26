"""
Utility functions to manipulate data, tables and dataframes.
"""
import os

import fbpyutils

# Setup logger and environment first
fbpyutils.setup(os.path.join(os.path.dirname(__file__), "app.json"))
env = fbpyutils.get_env()
logger = fbpyutils.get_logger()
