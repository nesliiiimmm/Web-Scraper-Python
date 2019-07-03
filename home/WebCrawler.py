import urllib

from home.CreateFile import CreateFile
from home.Parser import Parser
from home.CreateName import CreateName


def WebCrawler(items):
        path = CreateFile(items[0])
        newpath = "./Web Crawler/Text and Other/" + items[0] + "/Pdf/"
        i = items[1]
        if("ikipedia" in i):
            return
        if(i[len(i) - 4:] == '.pdf'):
            pdfname=CreateName(i)
            urllib.request.urlretrieve(i, newpath + pdfname)
        else:
            try:
                Parser(i, items[0],path)
            except:
                print("Bu siteye girilemedi:"+i)



