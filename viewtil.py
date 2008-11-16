def user_url(user):
  return '/users/%s' % user

import jinja2
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), line_statement_prefix="#")
env.filters['user_url'] = user_url
env.filters['len'] = len


def render(template,**args):
  return env.get_template(template+'.html').render(**args)


from settings import db
import dbviews
import web
def get_you():
  openid = web.openid.status()
  if openid:
    key = "user-%s" % openid
    if key in db:
      return db[key]
    else:
      you = {'type':'user', 'openids':[openid], 'name':'anonymous'}
      db[key] = you
      return you
