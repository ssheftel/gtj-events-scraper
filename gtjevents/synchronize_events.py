#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""module for synchronize events from gtj site to the data service database"""

import os
from .page import Page, GtjPage
from .event_finder import get_event_urls_for_events_within_n_months
from .event_scraper import EventScraper
from .data_service_client import get_saved_event_identifiers_from_db
import requests
import logging
import json


logger = logging.getLogger('mainlog'+'.'+__name__)
logger.info('running synchronize_events')

DATA_SERVICE_EVENTS_URL = os.environ.get('DATA_SERVICE_EVENTS_URL')
SYNCHRONIZE_NEXT_N_MONTHS = int(os.environ.get('SYNCHRONIZE_NEXT_N_MONTHS'))

def get_new_and_updated_events():
  """scrape the next n months calendard return dict with all updated new and 
  already processed events information"""

  already_stored_events = []
  updated_events = {} # maps existing _id to EventScraper
  updated_events_etags = {} # must pass etag, updated events _id
  new_events = []
  (saved_events_urls_and_doc_ids, hashes, id_with_etag_map) = get_saved_event_identifiers_from_db()
  event_urls_for_next_n_months = get_event_urls_for_events_within_n_months(SYNCHRONIZE_NEXT_N_MONTHS)
  for event_url in event_urls_for_next_n_months:
    event = EventScraper.from_url(event_url)
    if event.hash in hashes:
      already_stored_events.append(event)
    elif event.url in saved_events_urls_and_doc_ids:
      doc_id = saved_events_urls_and_doc_ids[event.url]
      etag = id_with_etag_map[doc_id]
      event.etag = etag
      updated_events[doc_id] = event
    else:
      new_events.append(event)

  found_events_by_sync_status = {
    'new_events': new_events,
    'updated_events': updated_events,
    'already_stored_events': already_stored_events
  }
  return found_events_by_sync_status

def post_new_events(new_events_scraps):
  """takes list of event_scraps and preformes a bulk save of them to the database"""
  results = {'error':[], 'saved':[], 'updated': []}
  if not new_events_scraps: return results
  new_events_data = [new_event_scrape.to_dict() for new_event_scrape in new_events_scraps]
  new_events_urls = [new_event_scrape.url for new_event_scrape in new_events_scraps] # for logging
  logger.info('about to post %s new events from urls %s', str(len(new_events_urls)), new_events_urls)
  payload = json.dumps(new_events_data)
  r = requests.post(
    DATA_SERVICE_EVENTS_URL,
    data=payload,
    headers={'Content-Type': 'application/json'}
  ) # add authentication
  if not r.ok:
    logger.error('Error while saving new events - post_new_events: %s, urls=%s', r.text, new_events_urls)
    results['error'] = new_events_scraps
    return results
  results['saved'] = new_events_scraps
  return results

def update_existing_events(updated_events_dict):
  """update mondifed event"""
  results = {'error': [], 'saved': [], 'updated': []}
  if not updated_events_dict: return results
  for _id, event_scrap in updated_events_dict.items():
    update_url = '{DATA_SERVICE_EVENTS_URL}/{_id}'.format(DATA_SERVICE_EVENTS_URL=DATA_SERVICE_EVENTS_URL, _id=_id)
    payload = json.dumps(event_scrap.to_dict())
    headers = {'Content-Type': 'application/json', 'If-Match': event_scrap.etag}
    logger.info('about to update event with _id= %s', _id)
    r = requests.patch(
      update_url,
      data=payload,
      headers=headers
    )
    if not r.ok:
      logger.error('Error while updating event with _id= %s urls= %s', _id, update_url)
      results['error'].append(event_scrap) # TODO: figure way to add _id
    else:
      results['updated'].append(event_scrap) # TODO: figure way to add _id
  return results

def synchronize_events():
  """main method for scraping site detecting new and updated events and storing theses
  returns a dict with the urls for the events that were saved, updated and which errored out
  return dict structure = {'error': [], 'saved': [], 'updated': []}"""
  sync_results = {'error': [], 'saved': [], 'updated': []} # TODO add _id of updated events
  found_events = get_new_and_updated_events()
  new_events = found_events['new_events']
  updated_events = found_events['updated_events']
  already_stored_events = found_events['already_stored_events']
  logger.info('running synchronize_events with %s new_events, %s updated_events, %s already_stored_events', len(new_events), len(updated_events), len(already_stored_events))

  #save and update events
  post_new_events_results = post_new_events(new_events)
  update_existing_events_results = update_existing_events(updated_events)
  
  # merge save and update result dicts into sync_results
  for error_result in post_new_events_results['error']:
    sync_results['error'].append(error_result.url)
  for saved_result in post_new_events_results['saved']:
    sync_results['saved'].append(saved_result.url)
  for updated_result in post_new_events_results['updated']:
    sync_results['updated'].append(updated_result.url)
  for error_result in update_existing_events_results['error']:
    sync_results['error'].append(error_result.url)
  for saved_result in update_existing_events_results['saved']:
    sync_results['saved'].append(saved_result.url)
  for updated_result in update_existing_events_results['updated']:
    sync_results['updated'].append(updated_result.url)
  return sync_results











