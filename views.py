import settings
import couchdb
import dbviews
server = couchdb.Server(settings.server)
db = server[settings.dbname]

def user_url(user):
  return '/%s' % user

import jinja2
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), line_statement_prefix="#")
env.filters['user_url'] = user_url


def render(template,**args):
  print env.get_template(template+'.html').render(**args)


class user:
  def GET(self, user):
    things = [row.value for row in db.query(dbviews.map_things, startkey=user, endkey=user, count=10)]
    render('user', user=user, things=things)

class index:
  def GET(self):
    users = [row.key for row in db.query(dbviews.map_users, dbviews.reduce_nothing, group=True)]
    render('index',users=users)