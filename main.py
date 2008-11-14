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

def unique(list,attr):
  #print list
  return dict((obj[attr], obj) for obj in list).values()


class FurAffinityScraper:
  def parse_user(self,user):
    base = "http://furaffinity.net"
    galleries = ["/gallery/" + user,"/scraps/" + user]
    
    things = []
    for gallery in galleries:
      for page in xrange(1,999):
        page_str = "/%d" % page
        gallery_page = get(base + gallery + page_str)
        new_things = gallery_page.findAll('a',href=re.compile("/view/"))
        if len(new_things) == 0: break
        things.extend(new_things)

    return unique(things,'href')

class ArtSpotsScraper:
  def __init__(self):
    pass

  def parse_user(self,user):
    base = "http://%s.artspots.com" % user

    user_page = get(base)
    galleries = user_page.findAll('a',href=re.compile("/gallery/"))
    galleries = unique(galleries,'href')

    things = []
    for gallery in galleries:
      page_str = "?per_page=100"
      gallery_page = get(base + gallery['href'] + page_str)
      new_things = gallery_page.findAll('a',href=re.compile("/image/"))
      things.extend(new_things)

    return unique(things,'href')


#for thing in ArtSpotsScraper().parse_user('malaikawolfcat'):
#  print thing['href']

for thing in FurAffinityScraper().parse_user('renardv'):
  print thing['href']

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
