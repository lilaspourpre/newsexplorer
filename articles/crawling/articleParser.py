# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, cookielib
import re

class ArticleParser:
    def RussianParser(self, url):
        con = urllib2.urlopen(url)
        HTML = con.read()
        soup = BeautifulSoup(HTML, 'html.parser')
        title = soup.findAll(attrs={'class' : 'b-article__title'})[0].get_text()
        text = ''
        pText = re.compile(r'<.+>.+</.+>')
        for hit in soup.findAll(attrs={'itemprop' : 'articleBody'}):
            for hit.p in hit:
                try:
                    if (unicode(hit.p)[:3]=='<p>'):
                        body = unicode(hit.p)[3:-4]
                    else:
                        body = unicode(hit.p)
                    body = pText.sub('',body)
                    if not body.startswith("<") and len(body)>1:
                        text+=body
                except:
                    pass
        text=text[1:]
        return (title, text)

    def EnglishParser(self, url):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        request = urllib2.Request(url)
        response = opener.open(request)
        HTML = response.read()
        soup = BeautifulSoup(HTML, 'html.parser')
        try:
            title = soup.findAll(attrs={'class' : 'kicker'})[0].get_text()
            text = ""
            webText = soup.find_all(attrs={'class' : "story-body-text story-content"})
            for i in webText:
                text += i.get_text()+"\n"
            return (title,text)
        except:
            pass