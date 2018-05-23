from bs4 import BeautifulSoup
import codecs
import re
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ArticleGetter:
    list_of_articles = []

    def GetEnglishArticles(self):
        index = 1
        while len(self.list_of_articles)<401:
            self.UrlConstructor(index)
            index +=1
            print("Now I have " + str(len(self.list_of_articles)) + " articles!")
        #and then write them to file

        for l in self.list_of_articles:
            with codecs.open("listOfArticlesEN.txt", 'a') as f:
                f.write(l + "\n")


    def UrlConstructor(self, index):
        url = "https://query.nytimes.com/search/sitesearch/?action=click&region=Masthead&pgtype=SectionFront&module=SearchSubmit&contentCollection=us&t=qry222#/*/30days/allresults/"+str(index)+"/allauthors/relevance/World/"
        l = self.CheckValid(url)

        for l1 in l:
            self.list_of_articles.append(l1)

    def CheckValid(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        list = []
        els = driver.find_elements_by_tag_name("a")
        for el in els:
            h = el.get_attribute("href")
            if h is not None:
                list.append(h)

        driver.close()
        return list[3:13]



a = ArticleGetter()
a.GetEnglishArticles()