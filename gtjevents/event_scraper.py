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





