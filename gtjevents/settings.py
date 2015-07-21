#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""settings script"""

import os
from dotenv import load_dotenv
import logging

MODULE_PATH = os.path.abspath(__file__)
MODULES_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(MODULES_DIR, '..'))
ENV_FILE_PATH = os.path.abspath(os.path.join(PARENT_DIR, '.env'))

if os.path.isfile(ENV_FILE_PATH):
  load_dotenv(ENV_FILE_PATH)


logger = logging.getLogger('mainlog')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
