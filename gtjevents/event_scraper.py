#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from bs4 import BeautifulSoup as bs
import re

class EventScraper(object):
  def __init__(self, page):
    """"""
    self._page = page
    self.url = page.location
    self.sp = bs(page.main_content)

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

  @property
  def gcal_url(self):
      """get gcal url"""
      gcal_tag = self.sp.select_one('.tribe-events-cal-links a.tribe-events-gcal')
      if not gcal_tag: return ''
      return gcal_tag.get('href', '')

  @property
  def post_id(self):
      """gets the post-id from main content id or None"""
      re.compile('post-(?P<num>\d+)')
      post_id_tags = self.sp.select('div[id^="post-"]')
      if not len(post_id_tags): return None
      for post_id_tag in post_id_tags:
        post_id = post_id_tag.get('id', '')
        post_id_pattern_match = re.match( 'post-(?P<num>\d+)', post_id)
        if post_id_pattern_match:
          post_id_num = int(post_id_pattern_match.groupdict().get('num', '0'))
          if post_id_num:
            return post_id_num
      return post_id_tag.get('id', None)

  @property
  def has_thumbnail(self):
    """bool whether event has thumbnail"""
    post_thumbnail_tag = self.sp.select_one('div.type-tribe_events.has-post-thumbnail')
    if not post_thumbnail_tag: return False
    return True

