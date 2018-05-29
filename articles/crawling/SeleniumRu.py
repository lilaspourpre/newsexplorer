 # -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import codecs

def getLinks():
    driver = webdriver.Chrome()
    driver.get("https://ria.ru/politics/")

    elements = driver.find_elements_by_tag_name("from_dot")


    while len(driver.find_elements_by_class_name("b-list__item"))<400:
        elements = driver.find_elements_by_tag_name("a")
        for i in elements:
            if i.get_attribute("data-ajax")!=None:
                i.click()
    lst = []
    elem = driver.find_elements_by_class_name("b-list__item")
    for el in elem:
        lst.append(el.find_element_by_tag_name("a").get_attribute("href"))
    print(len(lst))
    driver.close()
    return lst

for url in getLinks():
    with codecs.open("listOfArticlesRU.txt", 'a') as f:
        f.write(url + "\n")
