from settings import db
import web
import couchdb
import dbviews
from viewtil import render, get_you

class credits:
  def GET(self):
    return render('credits', you=get_you())
      
class things:
  def GET(self, username):
    for row in db.query(dbviews.map_users, startkey=username, endkey=username):
      user = row.value
      print user
      break
      
    things = []
    if 'accounts' in user:
      for account in user['accounts']:
        for row in db.query(dbviews.map_things, startkey=account, endkey=account):
          things.append(row.value)
      
    return render('user', user=user, things=things, you=get_you())

class index:
  def GET(self):
    users = [row.key for row in db.query(dbviews.map_users)]
    return render('index',users=users, you=get_you())

# Note: this may have to be changed if we make the form repeatable on the page
account_forms = 10
class settings:
  def GET(self):
    from scrapers import scrapers
    return render('settings', you=get_you(), scrapers=scrapers.keys(), account_forms=account_forms)
    
  def POST(self):
    you = get_you()
    params = web.input()
    
    accounts = []
    for x in xrange(account_forms):
      type = params['type-%d' % x]
      user = params['user-%d' % x]
      if type and user:
        accounts.append({'type':type,'user':user})
        
    you['accounts'] = accounts
    you['name'] = params['name']
    db[you.id] = you
    
    from scraper import Scraper
    Scraper(you).start()
    
    web.redirect('/')


urls = (
  '/', index,
  '/login', web.openid.host,
  '/settings', settings,
  '/credits', credits,
  '/users/(.*)', things,
)

application = web.application(urls, locals())