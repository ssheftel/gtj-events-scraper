#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from bs4 import BeautifulSoup as bs
import re
from dateutil import tz
from arrow import Arrow

class EventScraper(object):
  gcal_url_date_time_pattern = re.compile('(?:dates=)([\dT]+)\/([\dT]+)(?:&)')
  gcal_url_date_time_format = '%Y%m%dT%H%M%S' # example: 20150724T180000
  event_timezone = tz.gettz('US/Eastern')
  output_date_str_format = '%Y-%m-%dT%H:%M:%S.%fZ' # same as by mongo
  def __init__(self, page):
    """"""
    self._page = page
    self.url = page.location
    self.sp = bs(page.main_content)
    self._details_section = self.sp.select_one('div.tribe-events-meta-group.tribe-events-meta-group-details')
    self._organizer_section = self.sp.select_one('div.tribe-events-meta-group.tribe-events-meta-group-organizer')
    self._venue_section = self.sp.select_one('div.tribe-events-meta-group.tribe-events-meta-group-venue')
    self._gcal_url = None
    self._start_date_arrow = None
    self._end_date_arrow = None

  def __repr__(self):
    """repr() TODO: """
    return "EventScraper({})".format(repr(self._page.hash))

  @property
  def title(self):
    """finds events title"""
    title_tag = self.sp.select_one('h2.entry-title')
    if not title_tag: return ''
    return title_tag.get_text()

  @property
  def image_url(self):
    """gets event image url"""
    image_tag = self.sp.select_one('.tribe-events-event-image img')
    if not image_tag: return ''
    return image_tag.get('src', '')

  def _process_gcal_url(self):
    """private method for setting/cacheing the _gcal_url"""
    gcal_tag = self.sp.select_one('.tribe-events-cal-links a.tribe-events-gcal')
    if not gcal_tag:
      self._gcal_url = ''
    else:
      self._gcal_url = gcal_tag.get('href', '')



  @property
  def gcal_url(self):
    """get gcal url - either from cached _gcal_url or extracts"""
    if self._gcal_url != None: return self._gcal_url
    self._process_gcal_url()
    return self._gcal_url

  def _process_dates(self):
    """internal method to parse the gcal_url for start and end date info and
      set the _start_date_arrow and _end_date_arrow to instances of arrow objs
    """
    #dont rerun if _start_date_arrow or _end_date_arrow is set or if gcal_url not found
    if (self._start_date_arrow or self._end_date_arrow) or not self.gcal_url: return
    gcal_url = self.gcal_url
    gcal_url_date_time_match = self.gcal_url_date_time_pattern.search(gcal_url)
    if not gcal_url_date_time_match: return
    (gcal_url_start_date_str, gcal_url_end_date_str) = gcal_url_date_time_match.groups()
    # add time to date if no time spesified
    if 'T' not in gcal_url_start_date_str: gcal_url_start_date_str += 'T000000'
    if 'T' not in gcal_url_end_date_str: gcal_url_end_date_str += 'T000000'
    self._start_date_arrow = Arrow.strptime(gcal_url_start_date_str, self.gcal_url_date_time_format, tzinfo=self.event_timezone)
    self._end_date_arrow = Arrow.strptime(gcal_url_end_date_str, self.gcal_url_date_time_format, tzinfo=self.event_timezone)

  def _arrow_date_formatter(self, arrow):
    """private method used to convert internal arrow date obj into date values"""
    return arrow.to('utc').strftime(self.output_date_str_format)

  @property
  def start_date(self):
    """start date time - datetime obj parsed from gcal_url"""
    self._process_dates()
    if self._start_date_arrow == None: return None
    return self._arrow_date_formatter(self._start_date_arrow)


  @property
  def end_date(self):
    """end date time - datetime obj parsed from gcal_url"""
    self._process_dates()
    if self._end_date_arrow == None: return None
    return self._arrow_date_formatter(self._end_date_arrow)

  @property
  def post_id(self):
    """gets the post-id from main content id or None"""
    post_id_tag_pattern = re.compile('^post-(?P<post_id>[1-9]\d*)')
    post_id_tag = self.sp.find('div', {'id': post_id_tag_pattern})
    if not post_id_tag: return None
    tag_id = post_id_tag.get('id')
    post_id = post_id_tag_pattern.match(tag_id).groupdict().get('post_id', 0)
    if not post_id: return None
    post_id = int(post_id)
    return post_id

  @property
  def has_thumbnail(self):
    """bool whether event has thumbnail"""
    post_thumbnail_tag = self.sp.select_one('div.type-tribe_events.has-post-thumbnail')
    if not post_thumbnail_tag: return False
    return True

  @property
  def category_classes(self):
    """event category classes"""
    category_classes = []
    class_pattern = re.compile('(tribe_events_)?cat((\-|\_)events)?(\-|\_)(?P<category_class>[\w\d\-]+)')
    tag_with_cat_classes = self.sp.find(attrs={'class':class_pattern})
    if not tag_with_cat_classes: return category_classes
    class_list = tag_with_cat_classes.get('class')
    for klass in class_list:
      match = class_pattern.match(klass)
      if not match: continue
      category_class = match.groupdict().get('category_class', '')
      category_class = category_class.strip()
      if category_class and category_class not in category_classes: # Could use Set here
        category_classes.append(category_class)
    category_classes.sort()
    return category_classes

  @property
  def descript_html(self):
    """event description html source"""
    descript_tag = self.sp.select_one('div.tribe-events-content.entry-content.description')
    if not descript_tag: return ''
    description_html = descript_tag.renderContents().strip()
    return description_html

  @property
  def description(self):
    """event descript plain text"""
    descript_tag = self.sp.select_one('div.tribe-events-content.entry-content.description')
    if not descript_tag: return ''
    description = descript_tag.text.strip().replace('\n', ' ')
    return description

  @property
  def facebook_event_url(self):
    """facebook event url - global search"""
    facebook_event_url_tag = self.sp.select_one('a[href^="https://www.facebook.com/events"]')
    if not facebook_event_url_tag: return ''
    facebook_event_url = facebook_event_url_tag.get('href', '')
    return facebook_event_url

  ###details###

  @property
  def event_website_url(self):
    """event_url from event details"""
    if not self._details_section: return ''
    event_website_url_tag = self._details_section.select_one('dd.tribe-events-event-url a')
    if not event_website_url_tag: return ''
    event_website_url = event_website_url_tag.get('href', '')
    return event_website_url

  @property
  def tags(self):
    """event tags from details section TODO: test page with tags"""
    tags = []
    if not self._details_section: return tags
    tags_ancor_tags = self._details_section.select('dd.tribe-event-tags a[href^="http://www.gatherthejews.com/tag/"]')
    if not tags_ancor_tags: return tags
    for tags_ancor_tag in tags_ancor_tags:
      tags.append(tags_ancor_tag.text().strip())
    return tags

  @property
  def cost(self):
    """event cost from details section - not store as string not int"""
    cost = ''
    if not self._details_section: return cost
    cost_tag = self._details_section.select_one('dd.tribe-events-event-cost')
    if not cost_tag: return cost
    cost = cost_tag.text.strip()
    return cost

  @property
  def start_date(self):
    """event start data and time - TODO: implement"""
    pass

  @property
  def end_date(self):
    """event end data and time - TODO: implement"""
    pass

  ###organizers###

  @property
  def organizer(self):
    """the name of the organization sponsoring the event - from organizer section"""
    if not self._organizer_section: return ''
    organizer_tag = self._organizer_section.select_one('dd.fn.org a')
    if not organizer_tag: return ''
    organizer = organizer_tag.text.strip()
    return organizer

  @property
  def organizers_profile_url(self):
    """organizers gtj profile page url from the organizer section"""
    if not self._organizer_section: return ''
    organizers_profile_url_tag = self._organizer_section.select_one('dd.fn.org a')
    if not organizers_profile_url_tag: return ''
    organizers_profile_url = organizers_profile_url_tag.get('href', '')
    return organizers_profile_url


  @property
  def organizers_phone(self):
    """organizers phone number from the organizer section - string"""
    if not self._organizer_section: return ''
    organizers_phone_tag = self._organizer_section.select_one('dd.tel')
    if not organizers_phone_tag: return ''
    organizers_phone = organizers_phone_tag.text.strip()
    return organizers_phone

  @property
  def organizers_email(self):
    """organizers email url from the organizer section"""
    if not self._organizer_section: return ''
    organizers_email_tag = self._organizer_section.select_one('dd.email')
    if not organizers_email_tag: return ''
    organizers_email = organizers_email_tag.text.strip()
    return organizers_email


  @property
  def organizers_website_url(self):
    """organizers website url from the organizer section"""
    if not self._organizer_section: return ''
    organizers_website_url_tag = self._organizer_section.select_one('dd.url a')
    if not organizers_website_url_tag: return ''
    organizers_website_url = organizers_website_url_tag.get('href', '')
    return organizers_website_url

  ###venue###

  @property
  def venue(self):
    """venue name from venue section"""
    if not self._venue_section: return ''
    venue_tag = self._venue_section.select_one('dd.author.fn.org a')
    if not venue_tag: return ''
    venue = venue_tag.text.strip()
    return venue

  @property
  def venue_url(self):
    """venue url attached to the venue name from venue section"""
    if not self._venue_section: return ''
    venue_url_tag = self._venue_section.select_one('dd.author.fn.org a')
    if not venue_url_tag: return ''
    venue_url = venue_url_tag.get('href', '')
    return venue_url

  @property
  def venue_website_url(self):
    """? venues website url ? - not sure how this differes from venue_url"""
    if not self._venue_section: return ''
    venue_website_url_tag = self._venue_section.select_one('dd.url a')
    if not venue_website_url_tag: return ''
    venue_website_url = venue_website_url_tag.get('href', '')
    return venue_website_url

  @property
  def venue_phone(self):
    """phone number of the venue from the venue section"""
    if not self._venue_section: return ''
    venue_phone_tag = self._venue_section.select_one('dd.tel')
    if not venue_phone_tag: return ''
    venue_phone = venue_phone_tag.text.strip()
    return venue_phone

  @property
  def gmap_url(self):
    """google maps link url from venue section"""
    if not self._venue_section: return ''
    gmap_url_tag = self._venue_section.select_one('dd.location a.tribe-events-gmap')
    if not gmap_url_tag: return ''
    gmap_url = gmap_url_tag.get('href', '')
    return gmap_url

  @property
  def address(self):
    """venue full text address"""
    if not self._venue_section: return ''
    address_tag = self._venue_section.select_one('dd.location address.tribe-events-address')
    if not address_tag: return ''
    address = address_tag.text.strip()
    return address

  @property
  def street(self):
    """street portion of the address from venue section"""
    if not self._venue_section: return ''
    street_tag = self._venue_section.select_one('dd.location address.tribe-events-address .street-address')
    if not street_tag: return ''
    street = street_tag.text.strip()
    return street

  @property
  def city(self):
    """city portion of the address from venue section"""
    if not self._venue_section: return ''
    city_tag = self._venue_section.select_one('dd.location address.tribe-events-address .locality')
    if not city_tag: return ''
    city = city_tag.text.strip()
    return city

  @property
  def state(self):
    """state portion of the address from venue section"""
    if not self._venue_section: return ''
    state_tag = self._venue_section.select_one('dd.location address.tribe-events-address .region.tribe-events-abbr')
    if not state_tag: return ''
    state = state_tag.text.strip()
    return state

  @property
  def zip(self):
    """zip code/postal code of the addess from venue section"""
    if not self._venue_section: return ''
    zip_tag = self._venue_section.select_one('dd.location address.tribe-events-address .postal-code')
    if not zip_tag: return ''
    zip = zip_tag.text.strip()
    return zip

  @property
  def country(self):
    """country section of the address from the venue section"""
    if not self._venue_section: return ''
    country_tag = self._venue_section.select_one('dd.location address.tribe-events-address .country-name')
    if not country_tag: return ''
    country = country_tag.text.strip()
    return country





















