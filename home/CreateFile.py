import os
def CreateFile(Name):
    path="./Web Crawler/Text and Other/"+Name+"/"
    tpath="./Web Crawler/"
    if not os.path.exists(tpath):
        os.mkdir(tpath)
    newpath = tpath + "ExchangeList/"
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    newpath = tpath + "PriceList/"
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    newpath = tpath + "Text and Other/"
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    if not os.path.exists(path):
        os.mkdir(path)
    newpath=path+"Images/"
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    newpath=path+"Pdf/"
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    newpath=path+"Videos/"
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    return path

