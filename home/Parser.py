from requests_html import HTMLSession
import urllib.request

from home.Analysis import Analysis
from home.CreateName import CreateName
from home.CreateUrl import CreateUrl


def Parser(url,SearchTerm,path):
    session = HTMLSession()

    r = session.get(url)
    #if (root != 1):
        #path = CreateFile(SearchTerm)

    ########İMAGE################
    aboutimg = r.html.find('img')
    newpath = path + "/Images/"
    file = open(newpath + SearchTerm + ".txt", "a")
    if (aboutimg != []):
        for abi in aboutimg:
            sayac = 0
            img = []
            try:
                alt = abi.attrs['alt']
                calt = Analysis(SearchTerm, alt)
                if (calt > sayac):
                    sayac = calt
            except:
                print(" There is no alt attrs...")
            try:
                title = abi.attrs['title']
                ctitle = Analysis(SearchTerm, title)
                if (ctitle > sayac):
                    sayac = ctitle
            except:
                print(" There is no title attrs...")
            try:
                img = abi.attrs['src']
                cimg = Analysis(SearchTerm, img)
                if (cimg > sayac):
                    sayac = cimg
            except:
                print(" There is no image attrs...")

            if (img != []):
                resimismi = CreateName(img)
            else:
                resimismi = SearchTerm

            if (sayac > 0):
                try:
                    urllib.request.urlretrieve(img, newpath + resimismi)
                    file.write(resimismi+"\n"+img+"\n")
                    file.write("______________________________________\n")
                except:
                    try:
                        simg = CreateUrl(url, img)
                        urllib.request.urlretrieve(simg, newpath + resimismi)
                        file.write(resimismi + "\n" + simg + "\n")
                        file.write("______________________________________\n")
                    except:
                        print('olmadı-> ' + img)
            else:
                print("kelime eşlenmesi sağlanmadı -> " + resimismi)
    else:
        print("There is no image")

    #######VİDEOO################

    aboutvideo = r.html.find('video')
    newpathVideo = path + "/Videos/"
    if (aboutvideo != []):
        for abv in aboutvideo:
            try:
                vdo = abv.attrs['src']
                if (vdo != []):
                    videoismi = CreateName(vdo)

                    try:
                        print("Video İndiriliyor....")
                        urllib.request.urlretrieve(vdo, newpathVideo + videoismi)
                        file.write(videoismi + "\n" + vdo + "\n")
                        file.write("______________________________________\n")
                    except:
                        print('olmadı-> ' + vdo)
            except:
                print("There is no src attrs....")
    else:
        print("There is no video")

    #######PDF################

    aboutHref = r.html.find('a')
    newpathPdf = path + "/Pdf/"

    if (aboutHref != []):
        for abp in aboutHref:
            try:
                href = abp.attrs['href']
                if (href != []):
                    if (href[len(href) - 4:] == '.pdf'):

                        pdfname = CreateName(href)

                        try:
                            urllib.request.urlretrieve(href, newpathPdf + pdfname)
                            file.write( pdfname+ "\n" + href + "\n")
                            file.write("______________________________________\n")
                        except:
                            try:
                                spdf = CreateUrl(url, href)
                                urllib.request.urlretrieve(spdf, newpathPdf + pdfname)
                                file.write(pdfname + "\n" +spdf  + "\n")
                                file.write("______________________________________\n")
                            except:
                                print('olmadı-> ' + spdf)
                    #elif(href[len(href) - 4:] != 'aspx'):#Linkleri toplamak için..
                    #    if(root==0):
                    #        try:
                    #            Parser(href,SearchTerm,1)
                    #        except:
                    #            try:
                    #                shref = urlOlustur(url, href)
                    #                Parser(shref,SearchTerm,1)
                    #            except:
                    #                print('olmadı-> ' + shref)
            except:
                print(" There is no href attrs...")
    else:
        print("There is no Link or Pdf")

    # final = HtmlText(u, SearchTerm)
    # if (final != []):
    #    file = open(path + SearchTerm + ".txt", "w")
    #    for k in final:
    #        file.write('Metin 1' + k + '\n')
    #    file.close()
# if(data!=[]):
# file=open(path + SearchTerm + ".txt", "w")
# for d in data:
#    file.write(d.name+"\n")
#    file.write(d.Text + "\n")
#    file.write(d.link + "\n")
#    file.write("______________________________\n")
# file.close()
# href=about[0].attrs['href']
# r=session.get(href)
# print(r.html.url)































