import web
web.webapi.internalerror = web.debugerror


if __name__ == "__main__":
  # Make sure environment variables are set!
  from os import environ
  if 'AMAZON_SECRET' in environ and 'AMAZON_KEY' in environ:
    from views import application
    application.run()
  else:
    print "Set your AMAZON_KEY and AMAZON_SECRET environment variables"