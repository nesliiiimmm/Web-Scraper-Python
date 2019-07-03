from django.shortcuts import render
from googleapiclient.discovery import *
from home.GetPrice import GetPrice
from multiprocessing import Pool
from home.GetText import GetText
from home.exchange import exchange
from home.WebCrawler import WebCrawler
from home.Control import Control
from fuzzywuzzy import fuzz


my_api_key = "AIzaSyC89O-yDadEzHUn6SllJkTd1dadyQnXQO0"
my_cse_id = "015054545797869500988:vly5-lebkde"


# Create your views here.
def home_view(request):
    return render(request, 'home.html', {})
def search(request, **kwargs):
    links=list()
    i = 1
    for k in range(3):
        search_term = request.GET['search']
        service = build("customsearch", "v1", developerKey=my_api_key,)
        res = service.cse().list(q=search_term, cx=my_cse_id, lr="lang_tr", start=i ,**kwargs).execute()
        items = [ress['link'] for ress in res['items'][:]]
        for j in items:
            links.append(j)
        i+=10

    if fuzz.token_set_ratio('exchange', search_term) > 70:
        return render(request, 'home.html', {'exchange': exchange(search_term)})
    else:
        linkler =list()
        for i in links:
            linkler.append((search_term, i))

        pool = Pool(processes=30)
        pool.map(WebCrawler,linkler)
        if (Control(search_term)>0):
            data = pool.map(GetPrice, linkler)
        else:
            data = pool.map(GetText, linkler)
        pool.terminate()
        pool.join()
        return render(request, 'search.html', {'search': data})

if __name__ == '__main__':
    search()
