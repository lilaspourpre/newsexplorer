# -*- coding: utf-8 -*-'
import pymorphy2
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

import Splitter
import keywordsRU

def getInfo(persons, text, lan, splitter=None):
    if splitter != None:
        textSent = text.split(u"\r\n")
    else:
        if lan == "RU":
            textSent = Splitter.split_into_sentences(text.replace(".", ". "))
        else:
            textSent = sent_tokenize(text)
    need_sentences = []
    print("text = ", textSent)
    for i in textSent:
        for person in persons:
            if person in i:
                need_sentences.append(i)
    return need_sentences

def getAdj(persons, text, lang):
    if lang == "RU":
        return keywordsRU.keyWords(persons,text)
    else:
        nouns = []
        numbers = []
        adjectives = []
        verbs = []
        for t in text:
            words = word_tokenize(t)
            words = pos_tag(words)
            for i in range(len(words)):
                form = words[i]
                prevPrev = words[i - 2] if i != 0 and i!=1 else "START"
                prev = words[i - 1] if i != 0 else "START"
                next = words[i + 1] if i != len(words) - 1 else "END"
                nextNext = words[i + 2] if i != len(words) - 1  and  i != len(words) - 2  else "END"
                if "CD" == form[1]:
                    if prev[1] == "IN" or prev[1]=="TO":
                        numbers.append(prev[0]+" "+form[0]+" "+next[0]+" "+nextNext[0])
                    elif "JJ" in next[1] and nextNext[1] == "NNP" :
                        numbers.append(form[0]+" "+next[0]+" "+nextNext[0])
                    else:
                        numbers.append(form[0] + " " + next[0])

                if form[0] in persons:
                    if "JJ" in prev[1]:
                        adjectives.append(prev[0])
                    if prev[1] == "NNP":
                        nouns.append(prev[0])
                    if prev[1]== "NNP" and "JJ" in prevPrev[1]:
                        adjectives.append(prevPrev[0] + " " + prev[0])
                    if next[0] == "is" and nextNext[0] == "a":
                        if words[i+3][1] == "JJ":
                            adjectives.append(words[i+3][0]+" "+words[i+4][0])
                        else:
                            adjectives.append(words[i + 3][0])
                    if next[0] == "is" and nextNext[1] == "NNP":
                        nouns.append(nextNext[0])

                else:
                    if form[1] == "NNP":
                        if form[0].capitalize() == form[0]:
                            if prev[1] == "IN" or prev[1]=="TO":
                                nouns.append(prev[0] + " " + form[0])
                            if prev[1] == "JJ":
                                nouns.append(prev[0] + " " + form[0])
                            else:
                                nouns.append(form[0])

                if "VB" in form[1]:
                    verbs.append(form[0])
    print("nouns = ", nouns)
    print("numbers = ", numbers)
    print("adjs = ", adjectives)
    print("verbs = ", verbs)
    return [set(nouns), set(numbers), set(adjectives), set(verbs)]


def hightlighter(listOfSent, names, nouns=None, numbers= None, adjs = None, verbs=None):

    for sent in range(len(listOfSent)):
        sentence = listOfSent[sent]
        sentence = sentence.replace(u'___\r\n', "")

        decodedNames = list(set(names))
        newNouns = []
        if nouns != None:
            for key in nouns:
                for p in decodedNames:
                    if key not in p:
                        continue
                    else:
                        break
                else:
                    newNouns.append(key)


        for pers in decodedNames:
            if pers in listOfSent[sent]:
                for i in pers.split(" "):
                    sentence = sentence.replace(i,
                                            '<span style="background: aqua">'
                                            + i + "</span>")

        if nouns != None:
            for key in newNouns:
                if " "+key+" " in listOfSent[sent]:
                    sentence = sentence.replace(key,
                                                '<span style="background: yellow">'
                                                + key + "</span>")

        if verbs != None:
            for verb in verbs:
                if " "+verb+" " in listOfSent[sent]:
                    sentence = sentence.replace(" "+verb+" ",
                                                    ' <span style="background: lime">'
                                                    + verb + "</span> ")

        if adjs != None:
            for adj in adjs:
                if " "+adj+" " in listOfSent[sent]:
                    sentence = sentence.replace(adj,
                                                    ' <span style="background: #f60">'
                                                    + adj + "</span> ")

        if numbers != None:
            for num in numbers:
                if " "+num+" " in listOfSent[sent]:
                    sentence = sentence.replace(num,
                                                    ' <span style="background: #f9c">'
                                                    + num + "</span> ")

        listOfSent[sent:sent + 1] = [sentence]
    return listOfSent