# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib3
import re

class ArticleParser:
    def RussianParser(self, url):
        http = urllib3.PoolManager()
        soup = BeautifulSoup(http.request('GET', url), 'html.parser')
        title = soup.findAll(attrs={'class' : 'b-article__title'})[0].get_text()
        text = ''
        pText = re.compile(r'<.+>.+</.+>')
        for hit in soup.findAll(attrs={'itemprop' : 'articleBody'}):
            for hit.p in hit:
                try:
                    if (hit.p[:3]=='<p>'):
                        body = hit.p[3:-4]
                    else:
                        body = hit.p
                    body = pText.sub('',body)
                    if not body.startswith("<") and len(body)>1:
                        text+=body
                except:
                    pass
        text=text[1:]
        return (title, text)

    def EnglishParser(self, url):
        http = urllib3.PoolManager()
        soup = BeautifulSoup(http.request('GET', url), 'html.parser')
        try:
            title = soup.findAll(attrs={'class' : 'kicker'})[0].get_text()
            text = ""
            webText = soup.find_all(attrs={'class' : "story-body-text story-content"})
            for i in webText:
                text += i.get_text()+"\n"
            return (title,text)
        except:
            pass