import settings
import web
import couchdb
import dbviews
server = couchdb.Server(settings.server)
db = server[settings.dbname]
from render import render

you_query = """
function(doc){
  if(doc.type == 'user'){
    doc.openids.forEach(function(openid){
      emit(openid, {"name":doc.name, "accounts":doc.accounts, "openids":doc.openids})
    })
  }
}"""


def get_you():
  openid = web.openid.status()
  if openid:
    possibles = db.query(you_query, startkey=openid, endkey=openid)
    if len(possibles) == 0:
      you = {'type':'user', 'openids':[openid], 'name':'anonymous', 'accounts':[]}
      db.create(you)
      return you
    else:
      for row in possibles:
        return row.value
  


class credits:
  def GET(self):
    return render('credits', you=get_you())
      
class user:
  def GET(self, user):
    things = [row.value for row in db.query(dbviews.map_things, startkey=user, endkey=user)]
    return render('user', user=user, things=things, you=get_you())

class index:
  def GET(self):
    users = [row.key for row in db.query(dbviews.map_users, dbviews.reduce_nothing, group=True)]
    return render('index',users=users, you=get_you())


urls = (
  '/', index,
  '/login', web.openid.host,
  '/credits', credits,
  '/users/(.*)', user,
)

application = web.application(urls, locals())