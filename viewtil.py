def user_url(user):
  return "/users/%s" % user['slug']

def you_link(user):
  if 'slug' in user and 'name' in user:
    return "<a href=\"%s\">%s</a>" % (user_url(user),user['name'])
  else:
    return "<a href=\"/you\">anonymous</a>"

def you_name(user):
  if 'name' in user:
    return user['name']
  else:
    return "you"

import jinja2
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), line_statement_prefix="#")
env.filters['user_url'] = user_url
env.filters['you_link'] = you_link
env.filters['you_name'] = you_name
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
      you = {'type':'user', 'openids':[openid]}
      db[key] = you
      return you
