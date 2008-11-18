from os import environ
import couchdb

server_url = 'http://localhost:5984'
db_name = 'artscraper'
aws_key =  environ['AMAZON_KEY']
aws_secret = environ['AMAZON_SECRET']
s3_bucket = db_name

server = couchdb.Server(server_url)

if db_name not in server:
  db.create(db_name)
db = server[db_name]

def view_sync():
  from dbviews import views
  from couchdb.design import ViewDefinition as View
  View.sync_many(db,views,remove_missing=True)