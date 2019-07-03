from datetime import timedelta
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import requests
import requests_cache
import csv
import os
import re


class Product():
    def __init__(self, name=None, price=None, link=None ):
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
        self.i = 0
        self.soup = " "
        self.h1 = list()

    # HTML Parser Methods
    def handle_starttag(self, startTag, attrs):
        if (startTag == "h1"):
            self.lsStartTags.append(startTag)
            self.i += 1

    def handle_endtag(self, endTag):
        if (endTag == "h1"):
            self.lsEndTags.append(endTag)
            self.i -= 1

    def handle_data(self, data):
        if (re.search("[{}:%#!]", data) == None):
            if (self.i):
                self.IsData.append(data)
                self.h1.append(data)
            elif (data.find("TL") != -1 or data.isdigit() or re.sub(r'\W', "", data).replace("TL", "").isdigit()):
                self.IsData.append(data)
def strip(s):
    return s.strip()

def GetPrice(items):
        search_term = items[0]
        links = items[1]
        parser = MyHTMLParser()
        product = Product()
        requests_cache.install_cache(cache_name="Price_Cache", expire_after=timedelta(weeks=1))
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
            headers = {'User-Agent': user_agent}
            proxiess = {'http': 'http://10.10.0.0:0000',
                        'https': 'http://120.10.0.0:0000'}
            r = requests.get(links, timeout=10, headers=headers, proxies=proxiess)
            print(r.from_cache)
            datas = r.text
            parser.soup = BeautifulSoup(datas, "html.parser")
            parser.feed(datas)

            parser.IsData = list(map(strip, parser.IsData))
            parser.h1 = list(map(strip, parser.h1))

            parser.IsData.append("\n")

            for j in range(len(parser.IsData) - 1):
                if (fuzz.token_set_ratio(search_term,parser.IsData[j]) > 40 and product.name == None and parser.IsData[j] in parser.h1):
                        product.name = parser.IsData[j]
                        try:
                            if (re.sub(r'\W', "", parser.IsData[j + 1]).replace("TL", "").isdigit() and re.sub(r'\W', "",parser.IsData[j + 2]).replace("TL", "").isdigit() and parser.IsData[j + 1].find("TL") != -1 and parser.IsData[j + 2].find("TL") != -1):  # teknosa
                                if (re.sub(r'\W', "", parser.IsData[j + 1]).replace("TL", "") > re.sub(r'\W', "",parser.IsData[j + 2]).replace("TL", "")):
                                    product.price = parser.IsData[j+2]
                                else:
                                    product.price = parser.IsData[j + 1]

                            elif (re.sub(r'\W', "", parser.IsData[j + 1]).replace("TL", "").isdigit() and parser.IsData[j + 1].find("TL") != -1):  # teknosa
                                    product.price = parser.IsData[j + 1]

                            elif (re.sub(r'\W', "", parser.IsData[j + 1]).isdigit() and parser.IsData[j + 2] == "TL"):  # n11
                                    product.price = parser.IsData[j + 1] + " " + parser.IsData[j + 2]

                            elif (re.sub(r'\W', "", parser.IsData[j + 1]).isdigit() and parser.IsData[j + 3] =="TL"):  # vatan
                                    product.price = parser.IsData[j + 1] + parser.IsData[j + 2] + " " + parser.IsData[j + 3]

                            elif (re.sub(r'\W', "", parser.IsData[j + 1]).isdigit() and "TL" in parser.IsData[j + 2] and parser.IsData[j + 2][0] == ","):  # akakçe
                                    product.price = parser.IsData[j + 1] + parser.IsData[j + 2]
                            else:
                                i = j + 1
                                while (i < len(parser.IsData) - 1):

                                    if ("TL" in parser.IsData[i] and re.sub(r'\W', "", parser.IsData[i]).replace("TL", "").isdigit()):  # gittigidiyor sitesi
                                        product.price = parser.IsData[i]
                                        break
                                    elif (parser.IsData[i] == "TL" and re.sub(r'\W', "", parser.IsData[i - 1]).replace("TL", "").isdigit()):  # turkcell
                                        product.price = parser.IsData[i - 1] + " " + parser.IsData[i]
                                        break
                                    else:
                                        i += 1
                        except:
                            #product.name = None
                            product.price="Fiyat Bulunamadı!"

                            break

            product.link = links

        except requests.exceptions.SSLError:
            product.name = "SSLError"
            product.price = "SSLError"
            product.link = links
        except requests.ConnectionError:
            product.name = "ConnectionError"
            product.price = "ConnectionError"
            product.link = links
        except requests.exceptions.ReadTimeout:
            product.name = "ReadTimeoutError"
            product.price = "ReadTimeoutError"
            product.link = links
        path = "./Web Crawler/PriceList/"
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path+'PriceList.csv', 'a+', newline='') as f:
            f.seek(0)
            thereader = csv.reader(f)
            thewriter = csv.writer(f)
            file_is_empty = os.stat(path+'PriceList.csv').st_size == 0
            if file_is_empty:
                thewriter.writerow(['NAME', 'PRICE', 'LINK'])
            data = list()
            for lines in thereader:
                data.append(lines[2])
            if (product.link not in data):
                thewriter.writerow([product.name, product.price, product.link])

        parser.IsData.clear()

        return product