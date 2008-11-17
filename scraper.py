import scrapers
import couchdb
import dbviews
from settings import db
import settings

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


def scrape(type,user):
  # we know we can stop when we discover a source page we've already scraped
  old_sources = {}
  for row in db.query(dbviews.map_things, startkey=user, endkey=user):
    old_sources[row.value['source']] = True

  for thing in scrapers.dispatch(type,user,old_sources):
    key = "thing-%s" % thing['source']
    thing['account'] = {'user':user, 'type':type}
    thing['type'] = 'thing'
    thing['thumb'] = s3_cache(thing['thumb'])
    db[key] = thing
    
    
from threading import Thread
class Scraper(Thread):
  def __init__(self, user):
    Thread.__init__(self)
    self.accounts = user.get('accounts',None)

  def run(self):
    for account in self.accounts:
      scrape(account['type'],account['user'])
    print "Finished"
