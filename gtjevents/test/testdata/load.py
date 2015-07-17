#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Loads up tests data for use in tests"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import page

TEST_DATA_DIR = os.path.abspath(os.path.dirname(__file__))
EVENT_FILES = ['page-1.html']

class TestData(object):
  def __init__(self, files):
    for (i, file_name) in enumerate(files):
      file_type = file_name[:file_name.find('-')]
      prop_name = '{file_type}_{index}'.format(file_type=file_type, index=i+1)
      pg = page.GtjPage.fromFile(os.path.join(TEST_DATA_DIR, file_name))
      setattr(self, prop_name, pg)
    #TODO: Clean up
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'calendar-1.html')), 'r') as f:
      self.cal_page_1 = f.read()


td = TestData(EVENT_FILES)
