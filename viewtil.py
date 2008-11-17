def user_link(name):
  if name:
    return "<a href=\"/users/%s\">%s</a>" % (name,name)

def you_link(name):
  if name:
    return user_link(name)
  else:
    return "<a href=\"/you\">anonymous</a>"

import jinja2
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), line_statement_prefix="#")
env.filters['user_link'] = user_link
env.filters['you_link'] = you_link
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
