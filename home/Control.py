

def Control(text):
    search=text.lower()
    if("fiyat" in search):
        return 1
    elif("price" in search):
        return 2
    elif("prıce" in search):
        return 2
    else:
        return 0
