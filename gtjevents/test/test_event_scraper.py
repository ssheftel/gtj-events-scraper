#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from gtjevents.event_scraper import EventScraper
from testdata.load import td

scrap_1 = EventScraper(td.page_1)


def test_scrap_stores_page():
  assert scrap_1._page == td.page_1

def test_subsections():
  assert bool(scrap_1._details_section) == True
  assert bool(scrap_1._organizer_section) == True
  assert bool(scrap_1._venue_section) == True

def test_scrap_get_title():
  assert scrap_1.title == 'Shabbat Under the Stars'

def test_scrap_get_event_image():
  assert scrap_1.image_url == 'http://www.gatherthejews.com/wp-content/uploads/2015/05/SUTS3.jpg'

def test_scrap_gcal_url():
  assert scrap_1.gcal_url == 'http://www.google.com/calendar/event?action=TEMPLATE&text=Shabbat+Under+the+Stars&dates=20150724T180000/20150724T200000&details=%3Cp%3EShabbat+Under+the+Stars+is+a+casual%2C+outdoor+service+held+at+Washington+Hebrew+Congregation+during+June%2C+July%2C+and+August.+It+is+more+relaxed+in+feel+than+traditional+Shabbat+services%2C+features+upbeat+music%2C+and+offers+worshippers+the+option+of+staying+for+an+informal%2C+family-style+dinner+afterward.%3C%2Fp%3E%3Cp%3EThe+cost+for+dinner+is+%2412+per+person+or+%2430+for+a+family+of+up+to+four+people.%3C%2Fp%3E&location=11810+Falls+Road+%2C+Potomac%2C+MD%2C+20854%2C+United+States&sprop=website:http://www.gatherthejews.com&trp=false'

def test_private_process_dates():
  assert scrap_1._start_date_arrow == None
  assert scrap_1._end_date_arrow == None
  scrap_1._process_dates()
  assert scrap_1._start_date_arrow.timestamp == 1437775200
  assert scrap_1._end_date_arrow.timestamp == 1437782400

def test_start_date():
  assert scrap_1.start_date == '2015-07-24T22:00:00.000000Z'

def test_end_date():
  assert scrap_1.end_date == '2015-07-25T00:00:00.000000Z'

def test_scrap_post_id():
  assert scrap_1.post_id == 73096

def test_scrap_has_thumbnail():
  assert scrap_1.has_thumbnail == True

def test_category_classes():
  assert scrap_1.category_classes == ['prayer', 'reform', 'shabbat']

def test_description_html():
  assert scrap_1.descript_html == b'<p>Shabbat Under the Stars is a casual, outdoor service held at Washington Hebrew Congregation during June, July, and August. It is more relaxed in feel than traditional Shabbat services, features upbeat music, and offers worshippers the option of staying for an informal, family-style dinner afterward.</p>\n<p>The cost for dinner is $12 per person or $30 for a family of up to four people.</p>'

def test_description_text():
  assert scrap_1.description == 'Shabbat Under the Stars is a casual, outdoor service held at Washington Hebrew Congregation during June, July, and August. It is more relaxed in feel than traditional Shabbat services, features upbeat music, and offers worshippers the option of staying for an informal, family-style dinner afterward. The cost for dinner is $12 per person or $30 for a family of up to four people.'

def test_facebook_event_url():
  """TODO: test event with facebook event link"""
  assert scrap_1.facebook_event_url == ''
def test_event_url():
  assert scrap_1.event_website_url == 'http://www.whctemple.org/SUTS'

def test_tags():
  assert scrap_1.tags == []

def test_cost():
  assert scrap_1.cost == '12-30'

def test_start_date():
  """TODO: implment"""
  assert True == True

def test_end_date():
  """TODO: implment"""
  assert True == True

def test_organizer():
  assert scrap_1.organizer == 'Washington Hebrew Congregation'

def test_organizers_profile_url():
  assert scrap_1.organizers_profile_url == 'http://www.gatherthejews.com/organizer/washington-hebrew-congregation-2/'

def test_organizers_phone():
  assert scrap_1.organizers_phone == '202-362-7100'

def test_organizers_email():
  """TODO: test with page that has a email"""
  assert scrap_1.organizers_email == ''

def test_organizers_website_url():
  assert scrap_1.organizers_website_url == 'http://www.whctemple.org'

def test_venue():
  assert scrap_1.venue == 'Washington Hebrew Congregation: Julia Bindeman Suburban Center'

def test_venue_url():
  assert scrap_1.venue_url == 'http://www.gatherthejews.com/venue/washington-hebrew-congregation-julia-bindeman-suburban-center/'

def test_venue_website_url():
  """TODO: test with event that has this field"""
  assert scrap_1.venue_website_url == ''

def test_venue_phone():
  assert scrap_1.venue_phone == '301-279-7505'

def test_gmap_url():
  assert scrap_1.gmap_url == 'http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q=11810+Falls+Road++Potomac+MD+20854+United+States'

def test_address():
  assert scrap_1.address == '11810 Falls Road , Potomac, MD 20854 United States'

def test_street():
  assert scrap_1.street == '11810 Falls Road'

def test_city():
  assert scrap_1.city == 'Potomac'

def test_state():
  assert scrap_1.state == 'MD'

def test_zip():
  assert scrap_1.zip == '20854'

def test_country():
  assert scrap_1.country == 'United States'

def test_geo():
  assert scrap_1.geo == {'coordinates': [-77.1900311, 39.0506456], 'type': 'Point'}
