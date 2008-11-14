"""
Ways to be smarter about this:
  when should we re-scrape?
  scrape submission urls until we find one we already know, then stop
  occasionally scrape for new galleries

"""




import re

def get(url):
  from BeautifulSoup import BeautifulSoup
  from urllib import urlopen
  return BeautifulSoup(urlopen(url).read())


class Gallery(object):
  all = {}

  def __init__(self,thing):
    self.tag = thing
    self.all[thing['href']] = self

class Thing(object):
  all = {}

  def __init__(self,thing):
    self.tag = thing
    self.all[thing['href']] = self

def pager(page,host):
  if re.search('furaffinity.net',host):
    return "/%d" % page
  elif re.search('artspots.com',host):
    return "?per_page=100&fi=%d" % ((page-1)*100)


host = "http://furaffinity.net"
user = "/user/kalu"

userpage = host = "http://malaikawolfcat.artspots.com"


class FurAffinityscraper:
  pass

class ArtspotsScraper
  pass

# scrape for galleries
html = get(userpage)
galleries = html.findAll('a',href=re.compile("/gallery/"))
for gallery in galleries:
  Gallery(gallery)

for gallery in Gallery.all:
    #for page in xrange(1,999):
    #page_str = pager(page,host)
    page_str = "?per_page=100"
    print host+gallery+page_str
    html = get(host + gallery + page_str)
    things = html.findAll('a',href=re.compile("/image/"))
    if len(things) == 0: break
    for thing in things:
      Thing(thing)

for thing in Thing.all:
  print thing


"""
from html.parser import HTMLParser
class Parser(HTMLParser):
  def __init__(self,pattern):
    HTMLParser.__init__(self)
    self.pattern = pattern



  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for attr in attrs:
        if attr[0] == 'href':
          href = attr[1]
          if re.search(self.pattern,href):
            yield(href)
    
parser = Parser('gallery')
parser.feed(html)
"""
#print().read())
#for line in get("http://furaffinity.net/user/kalu").readlines():
#  print(line)
