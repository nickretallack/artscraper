from os import environ

server = 'http://localhost:5984'
dbname = 'artscraper'
aws_key =  environ['AMAZON_KEY']
aws_secret = environ['AMAZON_SECRET']
s3_bucket = dbname