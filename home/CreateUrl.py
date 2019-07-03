def CreateUrl(url,WrongUrl):

    from home.CreateName import CreateName

    word = CreateName(url)
    num = len(url) - len(word)
    final = url[:num]
    ret = final + WrongUrl
    return ret

