#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Page Class"""

from bs4 import BeautifulSoup as bs
import requests
import hashlib

class Page(object):
  main_content_selector = ''
  def __init__(self, location, html):
    """"""
    self.location = location
    self.html = html
    self.main_content = ''
    self.main_content = self._get_main_content()
    self.hash = self._compute_hash()

  def _compute_hash(self):
    """helper method for computing hash from location and main_content"""
    s = self.location + str(self.main_content)
    return hashlib.sha1(s.encode()).hexdigest()

  def _get_main_content(self):
    """helper method to select the main content html str"""
    if self.main_content_selector:
      main_content_soup = bs(self.html).select_one(self.main_content_selector)
      if main_content_soup and main_content_soup.renderContents:
        return main_content_soup.renderContents()
    return ''

  @classmethod
  def fromUrl(cls, url):
    """construct Page instance from a url"""
    r = requests.get(url)
    #add log/check if not r.ok
    page = cls(url, r.text)
    return page

  @classmethod
  def fromFile(cls, file_path):
    with open(file_path,'r') as f:
      html = f.read()
    page = cls(file_path, html)
    return page

class GtjPage(Page):
  main_content_selector  = 'div#content'



