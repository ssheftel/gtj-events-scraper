#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""scraper worker - runs at regualr interval and launced by worker dyno"""

import schedule
import time
import os

from gtjevents import settings
from gtjevents.synchronize_events import synchronize_events

import logging


logger = logging.getLogger('mainlog'+'.'+__name__)
logger.info('running run_worker')

run_interval = int(os.environ.get('RUN_INTERVAL', 3))
run_time_scale = os,environ.get('RUN_TIME_SCALE', 'HOURS') # or MINS


if run_time_scale == 'MINS':
  schedule.every(run_interval).minutes.do(synchronize_events)
else:
  schedule.every(run_interval).hour.do(synchronize_events)

if __name__ == '__main__':
  while True:
    schedule.run_pending()
    time.sleep(1)
