import re

# Soupifies a webpage
def get(url):
  from lib.BeautifulSoup import BeautifulSoup
  from urllib import urlopen
  return BeautifulSoup(urlopen(url).read())

# not really needed, but might help some day
def unique(list,attr):
  return dict((obj[attr], obj) for obj in list).values()

#### SCRAPERS

def hola():
  print "hola"



def dispatch(network,*args,**kwargs):
  return scrapers[network](*args,**kwargs)



def furaffinity(user, old_sources):
  base = "http://furaffinity.net"
  galleries = ["/gallery/" + user,"/scraps/" + user]
  
  for gallery in galleries:
    for page in xrange(1,999):
      page_str = "/%d" % page
      gallery_page = get(base + gallery + page_str)
      things = gallery_page.findAll('a',href=re.compile("/view/"))
      if len(things) == 0: break
      for thing in things:
        source = base + thing['href']
        if source in old_sources: return
  
        thumb = thing.find('img')
        datum = {'source':source}
        datum['thumb'] = thumb['src']
        datum['title'] = thumb['alt']        
        yield datum

def artspots(user, old_sources):
  base = "http://%s.artspots.com" % user
  
  user_page = get(base)
  galleries = user_page.findAll('a',href=re.compile("/gallery/"))

  for gallery in galleries:
    page_str = "?per_page=100"
    gallery_page = get(base + gallery['href'] + page_str)
    things = gallery_page.findAll('a',href=re.compile("/image/"))
    for thing in things:
      source = thing['href']
      if datum['source'] in old_sources: return

      datum = {'source':source}
      thumb = thing.find('img')
      datum['thumb'] = thumb['src']
      datum['title'] = thumb['title']
      yield datum
      
      
scrapers = {
  'furaffinity':furaffinity,
  'artspots':artspots,
}
