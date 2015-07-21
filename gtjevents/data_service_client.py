#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""module for interfacing with the database"""

import os
import requests
import logging

logger = logging.getLogger('mainlog'+'.'+__name__)
logger.info('running data_service_client.py')

DATA_SERVICE_EVENTS_URL = os.environ.get('DATA_SERVICE_EVENTS_URL')


def get_existing_events_url_and_hash_fields():
  """returns object where "_items" is a array of dicts containing
  key event identifyer fields these are (url, hash, and _id)
  they will be accessible via the ["_items"] top-level key"""
  url_and_hashes_for_all_events = {}
  events_url = DATA_SERVICE_EVENTS_URL
  query_params = {'max_results': 2000, 'projection': '{"hash":1, "_id":1, "url":1, "_etag":1}'} # TODO: remove 2000 size Also add min date
  r = requests.get(events_url, params=query_params)
  if not r.ok:
    logger.error('error while getting existing events identifiers with url=%s, r.text=%s', r.url, r.text)
    return {}
  resp_data = r.json()
  return resp_data

def _get_set_of_all_saved_event_hashes(all_events):
  """takes a list of event dicts and returns a set with the hashes for each event"""
  return {event['hash'] for event in all_events}

def _get_saved_event_urls_and_document_ids(all_events):
  """takes list of all event dicts and returns a dict maping saved event urls to 
  the corisponding object _id's"""
  return {event['url']:event['_id'] for event in all_events}

def _get_id_and_etag_map(all_events):
  """"""
  return {event['_id']:event['_etag'] for event in all_events}


def get_saved_event_identifiers_from_db():
  """loads key info about already saved events - returns a tuple in the form 
  (dict[url]->_id, dict[hash]->_etag)"""
  saved_events_resp = get_existing_events_url_and_hash_fields()
  if not saved_events_resp: return (dict(), set())
  saved_events = saved_events_resp['_items']
  url_document_map = _get_saved_event_urls_and_document_ids(saved_events)
  hashes_and_etags = _get_set_of_all_saved_event_hashes(saved_events)
  id_with_etag_map = _get_id_and_etag_map(saved_events)
  return (url_document_map, hashes_and_etags, id_with_etag_map)
