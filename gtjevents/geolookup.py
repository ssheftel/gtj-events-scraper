#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""geopy wrapper"""

import os
import time
from . import settings
from geopy.geocoders import GoogleV3
import logging

logger = logging.getLogger('mainlog'+'.'+__name__)
logger.info('Running GoogleMapsGeoLookup')

GOOGLE_GEOCODER_API_KEY = os.environ.get('GOOGLE_GEOCODER_API_KEY')

class GoogleMapsGeoLookup(object):
  last_lookup_request = time.time()
  min_lookup_timout = 1/5 # google maps limits 5 request per sec
  _googleV3 = GoogleV3(api_key=GOOGLE_GEOCODER_API_KEY)

  def geocode(self, address):
    """get geopy.location.Location from address
    geopy.location.Location has props: 
    address, altitude, latitude, longitude, point, raw
    """
    logger.info('geocode looking up of %s', address)
    current_time = time.time()
    time_elapsed_since_last_lookup = current_time - self.last_lookup_request
    if time_elapsed_since_last_lookup < self.min_lookup_timout:
      time.sleep(self.min_lookup_timout - time_elapsed_since_last_lookup)
    try:
      resp = self._googleV3.geocode(address)
    except (Exception, e):
      logger.warn('error while looking up geocode %s', address)
      resp = None
    self.last_lookup_request = time.time()
    return resp

  def __call__(self, address):
    """call to instance == isntance.geocode(address) returns a geopy.location.Location instance"""
    return self.geocode(address)
