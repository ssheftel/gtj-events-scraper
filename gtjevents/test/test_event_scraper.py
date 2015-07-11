#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from gtjevents.event_scraper import EventScraper
from testdata.load import td

scrap_1 = EventScraper(td.page_1)


def test_scrap_stores_page():
  assert scrap_1._page == td.page_1

def test_scrap_get_title():
  assert scrap_1.title == 'Shabbat Under the Stars'

def test_scrap_get_event_image():
  assert scrap_1.image_url == 'http://www.gatherthejews.com/wp-content/uploads/2015/05/SUTS3.jpg'

def test_scrap_gcal_url():
  assert scrap_1.gcal_url == 'http://www.google.com/calendar/event?action=TEMPLATE&text=Shabbat+Under+the+Stars&dates=20150724T180000/20150724T200000&details=%3Cp%3EShabbat+Under+the+Stars+is+a+casual%2C+outdoor+service+held+at+Washington+Hebrew+Congregation+during+June%2C+July%2C+and+August.+It+is+more+relaxed+in+feel+than+traditional+Shabbat+services%2C+features+upbeat+music%2C+and+offers+worshippers+the+option+of+staying+for+an+informal%2C+family-style+dinner+afterward.%3C%2Fp%3E%3Cp%3EThe+cost+for+dinner+is+%2412+per+person+or+%2430+for+a+family+of+up+to+four+people.%3C%2Fp%3E&location=11810+Falls+Road+%2C+Potomac%2C+MD%2C+20854%2C+United+States&sprop=website:http://www.gatherthejews.com&trp=false'

def test_scrap_post_id():
  assert scrap_1.post_id == 73096

def test_scrap_has_thumbnail():
  assert scrap_1.has_thumbnail == True



