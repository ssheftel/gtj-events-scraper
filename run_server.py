#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tornado server for manualy launching the scrapper"""


import os
import json
import tornado.ioloop
import tornado.web

from gtjevents import settings
from gtjevents import synchronize_events



class MainHandler(tornado.web.RequestHandler):
  def get(self):
    sync_results = synchronize_events.synchronize_events()
    self.write(json.dumps(sync_results))

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  host = os.environ.get('HOST', '127.0.0.1')

  application = tornado.web.Application([
    (r"/", MainHandler),
  ])
  application.listen(port, address=host)
  tornado.ioloop.IOLoop.current().start()
