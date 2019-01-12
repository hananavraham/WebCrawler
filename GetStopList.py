from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import codecs

TvShows = []
links = []

path = 'https://he.m.wikiquote.org/'
html = urlopen("https://he.m.wikiquote.org/wiki/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%94:%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA_%D7%98%D7%9C%D7%95%D7%95%D7%99%D7%96%D7%99%D7%94_%D7%99%D7%A9%D7%A8%D7%90%D7%9C%D7%99%D7%95%D7%AA")
soup = BeautifulSoup(html.read(), "lxml")

div = soup.find('div', attrs={'id':re.compile("mw-pages")})
pattern = r'"(.*?)"'

lis = div.find_all('ul') 
# collecting all tv shows links   
for li in div.find_all('li'):
    try:
        link = {}
        link["title"] = li.a.get_text()
        link["href"] = path + li.a['href']    #adding the start of the html path to each link
        
        links.append(link)
        
    except AttributeError:
        pass

# looping over all tv shows links and collect the expressions
for link in links:
    html = urlopen(link["href"])
    soup = BeautifulSoup(html.read(), "lxml")
    #div1 = soup.find('div', attrs ={'class':re.compile("mf-section-1"),'class':re.compile("collapsible-block")})
    div1 = soup.find_all('div',attrs={'class':re.compile("mf-section"),'class':re.compile("collapsible-block")})
    TvShow = {}
    sentences = []
    try:   
        for div in div1:
            for li in div.find_all('li'):
                sentence = {}            
                match = re.findall(pattern, li.get_text())
                if match:
                    sentence["text"] = match[0]
                    sentences.append(sentence)            
    except AttributeError:
        pass
   
    TvShows.append({'TvShow':link["title"],'sentences':sentences})    

to_save = json.dumps(TvShows, ensure_ascii=False)
with codecs.open('stopList.json', 'wb', encoding='utf-8') as f:
    f.write(to_save)