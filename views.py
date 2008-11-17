from settings import db
import web
import couchdb
import dbviews
from viewtil import render, get_you

class credits:
  def GET(self):
    return render('credits', you=get_you())

class you:
  def GET(self):
    you = get_you()
    things = user_things(you)
    return render('user', user="your", things=things, you=you, name="Your")


def user_things(user):
  things = []
  if 'accounts' in user:
    for account in user['accounts']:
      for row in db.query(dbviews.map_things, startkey=account, endkey=account):
        things.append(row.value)
  return things

class user:
  def GET(self, user_slug):
    if not user_slug:
      return "Not Found"

    user = None
    for row in db.query(dbviews.map_users, startkey=user_slug, endkey=user_slug):
      user = row.value
      print user
      break
    
    if not user:
      return "Not Found"
    
    things = user_things(user)
    name = user['name'].capitalize()
    return render('user', user=user, things=things, you=get_you(), name=name)

class index:
  def GET(self):
    users = [row.value for row in db.query(dbviews.map_users) if 'slug' in row.value]
    return render('index',users=users, you=get_you())

# Note: this may have to be changed if we make the form repeatable on the page
account_forms = 12
class settings:
  def GET(self):
    from scrapers import scrapers
    return render('settings', you=get_you(), scrapers=scrapers.keys(), account_forms=account_forms)
    
  def POST(self):
    you = get_you()
    params = web.input()
    
    # set accounts
    accounts = []
    for x in xrange(account_forms):
      type = params['type-%d' % x]
      user = params['user-%d' % x]
      if type and user:
        accounts.append({'type':type,'user':user})        
    you['accounts'] = accounts

    # set name - must be either blank (no userpage) or uniquely sluggifiable (unique url)
    unique = True
    name = params['name']
    if name and name != you.get('name',None):
      slug = slugify(name)
      for row in db.query(dbviews.map_slugs):
        if slug == row.key:
          unique = False
          break
    
      if unique:
        you['name'] = name
        you['slug'] = slug
    elif not name and 'name' in you:
      # blanking your name makes you anonymous, and makes your page inaccessible
      del you['name']
      del you['slug']
    
    db[you.id] = you
    
    from scraper import Scraper
    Scraper(you).start()

    if unique:
      web.redirect('/')
    else:
      from scrapers import scrapers
      return render('settings', errors="Sorry, that name's taken!", you=get_you(), scrapers=scrapers.keys(), account_forms=account_forms)


# Modified slugging routines originally stolen from patches to django
def slugify(value):
  """ Normalizes string, converts to lowercase, removes non-alpha characters,
  and converts spaces to hyphens.  """
  import unicodedata
  import re
  #value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
  value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
  return re.sub('[-\s]+', '-', value)


urls = (
  '/', index,
  '/login', web.openid.host,
  '/settings', settings,
  '/credits', credits,
  '/users/(.*)', user,
  '/you', you,
)

application = web.application(urls, locals())