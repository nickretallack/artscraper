from os import environ
import couchdb

server_url = 'http://localhost:5984'
db_name = 'artscraper'
aws_key =  environ['AMAZON_KEY']
aws_secret = environ['AMAZON_SECRET']
s3_bucket = db_name

server = couchdb.Server(server_url)
db = server[db_name]
