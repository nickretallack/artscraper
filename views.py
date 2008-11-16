from settings import db
import web
import couchdb
import dbviews
from viewtil import render, get_you

class credits:
  def GET(self):
    return render('credits', you=get_you())
      
class user:
  def GET(self, username):
    for row in db.query(dbviews.map_users, startkey=username, endkey=username):
      user = row.value
      break
      
    things = []
    for account in user['accounts']:
      network,name = account
      print network,name
      for row in db.query(dbviews.map_things): #db.query(dbviews.map_things, startkey=[name,network], endkey=[name,network]):
        print row
        things.append(row.value)
      print 'after'
      
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
      network = params['network-%d' % x]
      account = params['account-%d' % x]
      if account and network:
        accounts.append((network,account))
    you['name'] = params['name']
    you['accounts'] = accounts
    db[you.id] = you
    
    from scraper import Scraper
    Scraper(you).start()
    
    web.redirect('/')



class debug:
  def GET(self):
    return get_you()

urls = (
  '/', index,
  '/login', web.openid.host,
  '/settings', settings,
  '/credits', credits,
  '/users/(.*)', user,
  '/debug', debug,
)

application = web.application(urls, locals())