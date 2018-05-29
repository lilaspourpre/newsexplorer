# -*- coding: utf-8 -*-
import codecs
from nltk.tokenize import word_tokenize, sent_tokenize
import pymorphy2

class ruNER():

    def preprocessing(self, text):
        wordlist = word_tokenize(text) #splitting names
        sentences = sent_tokenize(text)
        animateObjects = self.posTagging(wordlist) #getting animObj with pymorphy2
        namesFormed = self.findPersonalNames(sentences, wordlist,animateObjects) #forming names
        return namesFormed

    def character_recognition(self, text):
        if '.txt' not in text:
            text+='.txt'
        text = codecs.open(text.encode("cp1251"), 'r', 'utf-8').read()
        return self.preprocessing(text.strip())

    def posTagging(self, sentences):
        animObjects = []
        for i in sentences:
            morph = pymorphy2.MorphAnalyzer()
            p = morph.parse(i)[0]
            if p.tag.POS == 'NOUN' and p.tag.animacy == "anim":
                animObjects.append(p.word)
        return animObjects

    def findPersonalNames(self, sentences, wordlist, animObjects):
        checkedWords = []
        checkedIndexes = []
        for n in range(len(wordlist)):
            wordPrev = wordlist[n-1] if n>=1 else "START"
            word = wordlist[n]
            wordNext = wordlist[n+1] if n < len(wordlist)-1 else "STOP"
            quotes = [u'``', u"''", u'´´', u"\"", u'«', u"‘", u"’", u"“", u"”", u"»", u"„", u"'"]
            morph = pymorphy2.MorphAnalyzer()
            if wordPrev not in quotes and wordNext not in quotes:
                if word.lower() in animObjects: #если содержится в списке одушевленных
                    if "ADJF" not in [morph.parse(word)[m].tag.POS for m in range(len(morph.parse(word)))]: #if it is not adj
                        if word.lower() not in [word_tokenize(i)[0].lower() for i in sentences]: #если не первое слово в предложении
                            if word == word.capitalize(): #если с заглавной
                                checkedWords.append(word)
                                checkedIndexes.append(n)

                            elif u"-" in word: #если в слове есть дефис
                                animWord = animObjects[animObjects.index(word.lower())] #searching for the word with dash - in list of animObjs
                                newAnimWord = animWord[:animWord.index("-")+1].capitalize()+animWord[animWord.index("-")+1::].capitalize() #для того, чтобы сравнить
                                #после дефиса мб заглавная буква
                                if word == newAnimWord:
                                    checkedWords.append(word)
                                    checkedIndexes.append(n)
                # else:
                #     if word == word.capitalize(): #смотрим, если слово с заглавной буквы и перед или после слово находится
                #         if n-1 in checkedIndexes or n+1 in checkedIndexes:
                #             print n
                #             checkedWords.append(word)
                #             checkedIndexes.append(n)
        return self.formPersonalNames(wordlist, checkedWords,checkedIndexes)

    def formPersonalNames(self, wordlistcount, checkedWords, checkedIndexes):
        #самое длинное если три и в нормальной форме, либо самое частоное если 1 - для кластера
        stoplist = [checkedIndexes[0]] #создаем кратковременный список, сразу кладем первый элемент id
        wordlist = [wordlistcount[checkedIndexes[0]]] #и кладем само слово тоже
        for i in checkedIndexes[1::]: #начинаем проверку с первого элемента
            if i == stoplist[len(stoplist)-1]+1 or len(stoplist)==0: #если следующий идет прямо за ним
                stoplist.append(i) #то мы продолжаем добавление
                wordlist.append(wordlistcount[i])
            else: #если нет
                checkedWords.append(" ".join(wordlist)) #то мы добавляем слова в список
                stoplist = [i] #очищаем списки
                wordlist = [wordlistcount[i]]
        checkedWords.append(" ".join(wordlist)) #после прохождения списка добавляем остаток
        return checkedWords


# ruNERc = ruNER()
# names = ruNERc.character_recognition(u"Богданов обсудил с президентом Сомали вопросы двусторонних отношений")
# for i in names.keys():
#     print i
#     for j in names.get(i):
#         print j,
#     print
#     print "***"