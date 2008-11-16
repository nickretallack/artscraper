import scrapers
import couchdb
import settings
server = couchdb.Server(settings.server)
db = server[settings.dbname]


def s3_cache(url):
  from urllib import urlopen
  from lib import S3
  s3 = S3.AWSAuthConnection(settings.aws_key, settings.aws_secret)
  data = urlopen(url)
  mime = data.info()
  sendable = S3.S3Object(data.read()) # could set metadata here
  headers = {'x-amz-acl':'public-read', 'Content-Type': mime.gettype()}
  print s3.put(settings.s3_bucket, url, sendable, headers).message
  return s3_url(url)

def s3_url(url):
  host = "http://s3.amazonaws.com"
  return "%s/%s/%s" % (host, settings.s3_bucket, url)


def scrape(network,user):
  for thing in scrapers.dispatch(network,user):
    thing['_id'] = thing['source']
    thing['thumb'] = s3_cache(thing['thumb'])
    db.update([thing])