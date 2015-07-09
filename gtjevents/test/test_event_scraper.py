#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from gtjevents import event_scraper


def test_scrap_has_src_prop():
	assert event_scraper.EventScraper('hi').src == 'hi'
