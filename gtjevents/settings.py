#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""settings script"""

import os
from dotenv import load_dotenv

MODULE_PATH = os.path.abspath(__file__)
MODULES_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(MODULES_DIR, '..'))
ENV_FILE_PATH = os.path.abspath(os.path.join(PARENT_DIR, '.env'))

load_dotenv(ENV_FILE_PATH)
