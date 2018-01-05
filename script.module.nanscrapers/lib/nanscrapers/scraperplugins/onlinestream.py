import re
import requests
import xbmc,time
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,filter_host

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class onlinestream(Scraper):
    domains = ['onlinestreammovies.com']
    name = "OnlineStream"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.onlinestreammovies.com'
        self.sources = []
        self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'ARB>>>'+ start_url
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('class="ml-item"><a href="(.+?)".+?oldtitle="(.+?)"',re.DOTALL).findall(html)
            #print 'PAGE>>>'+ html
            for item_url,name in Regex:
                if 'Hindi Dubbed' not in name:
                    if clean_title(title).lower() == clean_title(name).lower():
                        movie_link = item_url
                        #print 'LINK>>>'+ movie_link
                        self.get_source(movie_link,year)
                
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,movie_link,year):
        try:
            html = requests.get(movie_link).content
            chkdate = re.compile('<strong>Release:.+?rel="tag">(.+?)</a>',re.DOTALL).findall(html)[0]

            if year==chkdate:
                    uniques = []
                    links = re.compile('style="".+?href="(.+?)"',re.DOTALL).findall(html)
                    #print 'SOURCE>>>'+ html
                    for link in links:
                        if 'openload' in link:
                            try:
                                headers = {'User_Agent':User_Agent}
                                get_res=requests.get(link,headers=headers,timeout=5).content
                                rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                                if '1080p' in rez:
                                    qual = '1080p'
                                elif '720p' in rez:
                                    qual='720p'
                                else:
                                    qual='DVD'
                            except: qual='DVD' 
                            if link not in uniques:
                                uniques.append(link)
                                self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': link,'direct': False})
                            end_time = time.time()
                            total_time = end_time - self.start_time
                            print (repr(total_time))+"<<<<<<<<<<<<<<<<<<<<<<<<<"+self.name+">>>>>>>>>>>>>>>>>>>>>>>>>total_time"    
                        elif 'streamango.com' in link:
                            get_res=requests.get(link,headers=headers,timeout=5).content
                            rez = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                            if '1080' in rez:
                                qual = '1080p'
                            elif '720' in rez:
                                qual='720p'
                            else:
                                qual='DVD'
                            if link not in uniques:
                                uniques.append(link)
                                self.sources.append({'source': 'Streamango', 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
                            end_time = time.time()
                            total_time = end_time - self.start_time
                            print (repr(total_time))+"<<<<<<<<<<<<<<<<<<<<<<<<<"+self.name+">>>>>>>>>>>>>>>>>>>>>>>>>total_time"    
                        else:
                            #print 'OTHER '+link
                            try:
                                host = link.split('//')[1].replace('www.','')
                                host = host.split('/')[0].lower()
                                if not filter_host(host):
                                    continue
                                if link not in uniques:
                                    uniques.append(link)
                                    host = host.split('.')[0].title()
                                    self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': link,'direct': False})
                                end_time = time.time()
                                total_time = end_time - self.start_time
                                print (repr(total_time))+"<<<<<<<<<<<<<<<<<<<<<<<<<"+self.name+">>>>>>>>>>>>>>>>>>>>>>>>>total_time"     
                            except:pass
        except:
            pass

