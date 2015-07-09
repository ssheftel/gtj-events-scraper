#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Loads up tests data for use in tests"""

import os

TESTDATADIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(TESTDATADIR, 'event-1.html'), 'r') as f:
	event_1 = f.read()

