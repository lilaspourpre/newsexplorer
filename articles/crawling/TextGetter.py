# -*- coding: cp1251 -*-
import codecs
import os

import articleParser


class TextGetter():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

    def fileOpener(self, rel_path): #we open file
        abs_file_path = os.path.join(self.script_dir, rel_path)
        with codecs.open(abs_file_path, 'r') as f:
            material = f.read().split("\n")
        fileAdder = self.fileAdderEN if "EN" in rel_path else self.fileAdderRU #chose language
        for link in material: #call the function
            fileAdder(link)

    def fileAdderRU(self, link):
        newAParser = articleParser.ArticleParser()
        text = newAParser.RussianParser(link)
        print text[0]
        t = text[0].replace("\"", "")
        with codecs.open(self.script_dir+'/RUtexts/'+t.encode("cp1251")+'.txt', "a") as f:
            f.write(text[1].encode("utf-8"))

    def fileAdderEN(self, link):
        newAParser = articleParser.ArticleParser()
        if newAParser.EnglishParser(link)!=None:
            text = newAParser.EnglishParser(link)
            t = text[0].replace("|", "")
            t = t.replace("\.","")
            t = t.replace("\"","")
            try:
                with codecs.open(self.script_dir+"/ENtexts/"+t+".txt", "w") as f:
                    f.write(text[1].encode("utf-8"))
            except:
                with codecs.open(self.script_dir+"/ENtexts/"+t.split(" ")[0]+".txt", "w") as f:
                    f.write(text[0].encode("utf-8"))
                    f.write(text[1].encode("utf-8"))

rel_path_ru = "docs\\listOfArticlesRU.txt"
rel_path_en = "docs\\listOfArticlesEN.txt"

textGet = TextGetter()
textGet.fileOpener(rel_path_ru)