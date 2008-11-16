import settings
import couchdb
import dbviews
server = couchdb.Server(settings.server)
db = server[settings.dbname]

import web
web.webapi.internalerror = web.debugerror

urls = (
  '/', 'index',
  '/(.*)', 'user',
)

from render import render
class user:
  def GET(self, user):
    things = [row.value for row in db.query(dbviews.map_things, startkey=user, endkey=user, count=10)]
    render('user', user=user, things=things)

class index:
  def GET(self):
    users = [row.key for row in db.query(dbviews.map_users, dbviews.reduce_nothing, group=True)]
    render('index',users=users)


if __name__ == "__main__":
  # Make sure environment variables are set!
  from os import environ
  if 'AMAZON_SECRET' in environ and 'AMAZON_KEY' in environ:
    web.run(urls, globals(), web.reloader)
  else:
    print "Set your AMAZON_KEY and AMAZON_SECRET environment variables"




