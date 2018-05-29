# -*- coding: utf-8 -*-'
import pymorphy2
from nltk import word_tokenize


def keyWords(persons, text):
    nouns = []
    numbers = []
    adjectives = []
    verbs = []
    for t in text:
        words = word_tokenize(t)
        for i in range(len(words)):
            form = words[i]
            morph = pymorphy2.MorphAnalyzer()
            prevPrev = words[i - 2] if i!= 0 and i!=1 else "START"
            prev = words[i - 1] if i != 0 else "START"
            next = words[i + 1] if i != len(words) - 1 else "END"
            nextNext = words[i + 2] if i != len(words) - 1  and  i != len(words) - 2 else "END"
            prpr = morph.parse(prevPrev)[0]
            pr = morph.parse(prev)[0]
            ne = morph.parse(next)[0]
            w = morph.parse(form)[0]
            nene = morph.parse(nextNext)[0]

            if "NUMB" in w.tag:
                if pr.tag.POS == "PREP" and ne.tag.POS == "NOUN":
                    numbers.append(prev + " " + form + " " + next + " " + nextNext)
                elif ne.tag.POS == "ADJF" and nene.tag.POS == "NOUN":
                    numbers.append(form + " " + next + " " + nextNext)
                else:
                    numbers.append(form + " " + next + " " + nextNext)


            for pers in persons:
                if form == pers:
                    if prpr.tag.POS == "PREP" and pr.tag.POS == "ADJF":
                        adjectives.append(prevPrev + " " + prev)
                    elif pr.tag.POS == "ADJF":
                        adjectives.append(prev)
                    if ne.tag.POS == "ADJF":
                        adjectives.append(next)


                    if pr.tag.POS == "NOUN":
                        nouns.append(prev)
                    if pr.tag.POS == "NOUN" and prpr.tag.POS == "ADJF":
                        nouns.append(prevPrev + " " + prev)


            if w.tag.POS == "NOUN" and form.capitalize() == form:
                if pr.tag.POS == "PREP":
                    nouns.append(prevPrev + " " +prev + " " + form)
                else:
                    nouns.append(form)

            if "VERB" in w.tag:
                if ne.tag.POS == "PREP" and nene.tag.POS == "NOUN":
                    verbs.append(form + " " + next + " " + nextNext)
                else:
                    verbs.append(form)
            if "INFN" in w.tag:
                verbs.append(prevPrev+" "+prev+" "+form)

    print("nouns = ", nouns)
    print("numbers = ", numbers)
    print("adjs = ", adjectives)
    print("verbs = ", verbs)
    return [set(nouns) ,set(numbers), set(adjectives), set(verbs)]
