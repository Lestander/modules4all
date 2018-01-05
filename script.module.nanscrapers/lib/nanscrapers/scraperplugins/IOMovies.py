import re
import requests
import xbmc,time
import urllib
import HTMLParser
from ..scraper import Scraper
from ..common import clean_title,clean_search
from nanscrapers.modules import cfscrape
requests.packages.urllib3.disable_warnings()
User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'
clean_up = HTMLParser.HTMLParser()

class ionlinemovies(Scraper):
    domains = ['ionlinemovies.com']
    name = "ionlinemovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.ionlinemovies.com'
        self.scraper = cfscrape.create_scraper()
        self.sources = []
        self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'IO>>>> '+start_url
            headers = {'User_Agent':User_Agent}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            #print html
            Regex = re.compile('data-movie-id=.+?href="(.+?)".+?class="mli-info"><h2>(.+?)</h2>.+?rel="tag">(.+?)</a></div>',re.DOTALL).findall(html)
            for item_url,name,date in Regex:
                if clean_title(title).lower() == clean_title(name).lower():
                    if year in date:
                        movie_link = item_url
                        #print 'IO pass this > '+movie_link
                        self.get_source(movie_link)
                
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,movie_link):
        try:
            headers = {'User_Agent':User_Agent}
            html = self.scraper.get(movie_link).content
            source = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(html)[0]
            if 'consistent.stream' in source:
                headers = {'User_Agent':User_Agent}
                holder = requests.get(source,headers=headers,verify=False,timeout=5).content
                page = re.compile(""":title=["'](.+?)["']\>""").findall(holder)[0]
                decode = clean_up.unescape(page)
                sources= re.compile('"sources.+?"(http.+?)"',re.DOTALL).findall(decode)
                for link in sources:
                    link=link.replace('\\','')
                    #print 'link chk '+ link
                    if '1080' in link:
                        res='1080p'
                    elif '720' in link:
                        res = '720p'
                    else:
                        res = 'DVD'
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': link,'direct': False})
            end_time = time.time()
            total_time = end_time - self.start_time
            print (repr(total_time))+"<<<<<<<<<<<<<<<<<<<<<<<<<"+self.name+">>>>>>>>>>>>>>>>>>>>>>>>>total_time"        
        except:
            pass

