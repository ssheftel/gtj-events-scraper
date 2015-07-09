#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from gtjevents.event_scraper import EventScraper
import  testdata.load as td


def test_scrap_has_src_prop():
	assert EventScraper(td.event_1).src == td.event_1

def test_scrap_repr_can_be_evaled():
	scrp_1 = EventScraper(td.event_1)
	scrp_2 = eval(repr(scrp_1), globals())
	assert scrp_1.src == scrp_2.src



