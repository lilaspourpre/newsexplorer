# -*- coding: utf-8 -*-
import codecs
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize

class enNER():

    def character_recognition(self, text):
        if '.txt' not in text:
            text+='.txt'
        text = codecs.open(text, 'r', 'utf-8').read()
        text = text.replace(u"—", u"-")
        checkedNames = self.preprocessing(text.strip()) #pre process - pos tagging and ner, than name formatting
        return checkedNames

    def preprocessing(self, text):
        listOfNames = []
        sent = word_tokenize(text)
        nerWords = ne_chunk(pos_tag(sent), binary=False)
        for i in range(len(nerWords)):
            word = nerWords[i]
            if type(word)!=tuple:
                if "PERSON" in str(word):
                    listOfNames.extend([i[0] for i in word[0:]])
                    listOfNames.append(" ".join([i[0] for i in word[0:]]))

        return listOfNames

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
