#!/usr/bin/env python
import web
web.webapi.internalerror = web.debugerror
web.config.debug = True


if __name__ == "__main__":
  # Make sure environment variables are set!
  from os import environ
  if 'AMAZON_SECRET' not in environ or 'AMAZON_KEY' not in environ:
    print "Set your AMAZON_KEY and AMAZON_SECRET environment variables"
    
  from settings import view_sync
  view_sync()
    
  from views import application
  application.run()
