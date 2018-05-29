# -*- coding: utf-8 -*-
import re

def get_first_letter(word):
    for c in word:
        if c.isalnum():
            return c


def split_into_sentences(text):
    words = text.split()
    punc = {'.', '!', '?'}
    initial_punc = {'.', '"', "'", '«'}
    exceptions = {'т.н.', 'т.е.', 'т.к.', 'Т.н.', 'Т.е.', 'Т.к.'}
    sentences = []
    p = 0
    for w_i, w in enumerate(words):
        for c_i, c in enumerate(w):

            is_last_word = w_i == len(words) - 1
            is_last_char = c_i == len(w) - 1
            rest_not_alnum = not is_last_char and not w[c_i + 1:].isalnum()
            last_char_not_comma = w[-1] != ','
            first_letter = get_first_letter(words[w_i + 1]) if not is_last_word else ''
            next_word_capitalized = first_letter and first_letter.isupper()
            next_word_starts_digit = first_letter and first_letter.isdigit()
            not_exception = w not in exceptions
            not_initial = not re.match('[\'"«]*([А-Я]\.)+', w)

            condition1 = c in punc
            condition2 = (is_last_char or (rest_not_alnum and last_char_not_comma))
            condition3 = ((next_word_capitalized or next_word_starts_digit) and not_exception and not_initial)

            if is_last_word or (condition1 and condition2 and condition3):
                sentences.append(words[p:w_i + 1])
                p = w_i + 1
                break
    newSentences = []
    for sentence in sentences:
        newSentences.append(" ".join(sentence))
    return newSentences