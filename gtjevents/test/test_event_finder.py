#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from gtjevents.event_scraper import EventScraper
from gtjevents.event_finder import (get_nth_month_and_year, get_gtj_event_urls_for_month, get_gtj_month_calander_event_links, get_event_urls_for_events_within_n_months)
from testdata.load import td

cal_page_1 = td.cal_page_1


def test_get_nth_month_and_year():
  (month, year) = get_nth_month_and_year(0)
  assert month >= 7
  assert year >= 2015

def test_number_of_event_links():
  event_links = get_gtj_month_calander_event_links(cal_page_1)
  assert len(event_links) >= 73

def test_get_event_urls_for_events_within_n_months():
  """figure way to test but using loncal only env"""
  assert len(get_event_urls_for_events_within_n_months(2))  > 20

