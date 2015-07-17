#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""classes that walk sites and find event links"""

from bs4 import BeautifulSoup as bs
import datetime
import requests

gtj_event_link_selector = 'h3.tribe-events-month-event-title a.url'
gtj_calendar_url_template = 'http://www.gatherthejews.com/calendar/{year}-{month:02d}/'


def get_gtj_month_calander_event_links(month_calendar_html):
  """extracts event urls from gtj event month calendar - returns a set of urls"""
  event_urls = set()
  soup = bs(month_calendar_html)
  event_link_tags = soup.select(gtj_event_link_selector)
  for event_link_tag in event_link_tags:
    event_url = event_link_tag.get('href', '')
    if not event_url: continue
    event_urls.add(event_url)
  return event_urls

def get_gtj_event_urls_for_month(month, year):
  """gets all event urls for events during a given month and year returns a set"""
  url = gtj_calendar_url_template.format(month=month, year=year)
  req = requests.get(url)
  if not req or not req.text: return set
  month_calendar_html = req.text
  event_urls = get_gtj_month_calander_event_links(month_calendar_html)
  return event_urls

def get_nth_month_and_year(nth_month):
  """gets month and year corrisponding to a n months into the future returns (month, year)"""
  now = datetime.datetime.now()
  current_year = now.year
  current_month = now.month
  (year, month) = divmod((current_month+nth_month-1),12)
  month += 1
  year += current_year
  return (month, year)

def get_event_urls_for_events_within_n_months(number_of_months):
  """gets all event urls for events in the dext n months - returns a set of urls"""
  event_urls = set()
  for nth_month in range(number_of_months):
    (month, year) = get_nth_month_and_year(nth_month)
    nth_month_event_urls = get_gtj_event_urls_for_month(month, year)
    if not nth_month_event_urls: continue # TODO: add loging here
    event_urls.update(nth_month_event_urls)
  return event_urls

