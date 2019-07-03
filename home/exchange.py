from currency_converter import CurrencyConverter
import re
from fuzzywuzzy import fuzz
import csv
from datetime import date
import os

class Exc():
    def __init__(self, Amount=None, From = None, To=None,Result=None):
        self.Amount = Amount
        self.From = From
        self.To = To
        self.Result = Result

def exchange(search_term):
    parabirkod=[["DOLAR","USD"],["EURO","EUR"],["STERLIN","GBP"],["LIRA","TRY"],["ZLOTY","PLN"],
                ["RUBLE","RUB"],["FRANG","CHF"],["YUAN","CNY"],["YEN","JPY"],["KORUNA","CZK"],["TL","TRY"]]
    c = CurrencyConverter()
    exc = Exc()
    amount = re.sub(r'\D',"",search_term)
    if amount=="":
        amount=1
    search_term = search_term.upper().split(" ")
    exchange = list()
    exchange.append(amount)
    for crnt in search_term:
        for kod in parabirkod:
            if fuzz.token_set_ratio(crnt, kod[0]) > 70:
                exchange.append(kod[1])

    result = c.convert(amount, exchange[1], exchange[2]).__format__('.2f')
    exchange.append(result)
    path = "./Web Crawler/ExchangeList/"
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path +"ExchangeList.csv", "a", newline='') as f:
        thewriter = csv.writer(f)
        file_is_empty = os.stat(path+'ExchangeList.csv').st_size == 0
        if file_is_empty:
            thewriter.writerow(['AMOUNT', 'FROM', 'TO', "RESULT", "DATE"])
        thewriter.writerow([amount, exchange[1], exchange[2], result, date.today()])
        exc.Amount = amount
        exc.From = exchange[1]
        exc.To = exchange[2]
        exc.Result = result
    return exc







