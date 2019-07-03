from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re
import requests
import requests_cache
from fuzzywuzzy import fuzz
import os
from datetime import timedelta

class Text():
    def __init__(self, name=None, price=None, link=None):
        self.name = name
        self.price = price
        self.link = link

class MyHTMLParser(HTMLParser):

    # Initializing lists
    def __init__(self):
        HTMLParser.__init__(self)
        self.lsStartTags = list()
        self.lsEndTags = list()
        self.IsData = list()
        self.soup=" "
        self.i = 0

    def handle_data(self, data):
        if (re.search("[{}:!%#-]", data) == None ):
            self.IsData.append(data)

def GetText(linkler):
    text = Text()
    path = "./Web Crawler/Text and Other/" + linkler[0] + "/"
    if not os.path.exists(path):
        os.mkdir(path)
    file = open(path + linkler[0] + ".txt", "a")
    search_term = linkler[0]

    parser = MyHTMLParser()
    requests_cache.install_cache(cache_name="Text_Cache", expire_after=timedelta(weeks=1))
    text.price = " "
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        headers = {'User-Agent': user_agent}
        proxiess = {'http': 'http://10.10.0.0:0000',
                    'https': 'http://120.10.0.0:0000'}
        r = requests.get(linkler[1], timeout=5, proxies=proxiess, headers=headers)
        print(r.from_cache)
        datas = r.text
        parser.soup = BeautifulSoup(datas, "html.parser")
        parser.feed(datas)

        for i in parser.IsData:
            if(fuzz.token_set_ratio(search_term,i) > 70):
                file.write(i.strip().encode('utf-8')+"\n")
                text.price =text.price + i.strip() + "\n"

    except requests.exceptions.SSLError:
        file.write("SSLError !!!!\n")
    except requests.ConnectionError:
        file.write("ConnectionError !!!!\n")
    except requests.exceptions.ReadTimeout:
        file.write("ReadTimeoutError !!!!\n")
    except UnicodeEncodeError:
        file.write("UnicodeEncodeError\n")
    except NotImplementedError:
        file.write("NotImplementedError\n")
    file.write(linkler[1].encode('utf-8')+"\n")
    file.write("______________________________\n")
    text.name = linkler[0]
    text.link = linkler[1]

    return text