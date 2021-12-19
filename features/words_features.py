import csv
import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyse_sentence_score(inputtext):
    global analyzer

    if not "analyzer" in globals():
        analyzer = SentimentIntensityAnalyzer()

    score = analyzer.polarity_scores(inputtext)
    neg = score.get('neg')
    neu = score.get('neu')
    pos = score.get('pos')
    compound = score.get('compound')
    return_dict = {
        'values': [neg, neu, pos, compound],
        'heads': ['@Attribute analyse_sentence_neg REAL', '@Attribute analyse_sentence_neu REAL',
                  '@Attribute analyse_sentence_pos REAL', '@Attribute analyse_sentence_compound REAL']}
    return return_dict


def part_of_speech(inputtext):
    global sp

    if not "sp" in globals():
        sp = spacy.load("en_core_web_sm")

    sen = sp(inputtext)

    adj = 0
    adp = 0
    adv = 0
    aux = 0
    cconj = 0
    det = 0
    intj = 0
    noun = 0
    num = 0
    part = 0
    pron = 0
    propn = 0
    punct = 0
    sconj = 0
    sym = 0
    verb = 0
    x = 0

    for word in sen:
        if word.pos_ == "ADJ":
            adj = adj + 1
        if word.pos_ == "ADP":
            adp = adp + 1
        if word.pos_ == "ADV":
            adv = adv + 1
        if word.pos_ == "AUX":
            aux = aux + 1
        if word.pos_ == "CCONJ":
            cconj = cconj + 1
        if word.pos_ == "DET":
            det = det + 1
        if word.pos_ == "INTJ":
            intj = intj + 1
        if word.pos_ == "NOUN":
            noun = noun + 1
        if word.pos_ == "NUM":
            num = num + 1
        if word.pos_ == "PART":
            part = part + 1
        if word.pos_ == "PRON":
            pron = pron + 1
        if word.pos_ == "PROPN":
            propn = propn + 1
        if word.pos_ == "PUNCT":
            punct = punct + 1
        if word.pos_ == "SCONJ":
            sconj = sconj + 1
        if word.pos_ == "SYM":
            sym = sym + 1
        if word.pos_ == "VERB":
            verb = verb + 1
        if word.pos_ == "X":
            x = x + 1

    return_dict = {'values': [ adj, adp, adv, aux, cconj, det, intj, noun, num, part, pron, propn, punct, sconj, sym, verb, x],
                   'heads': ['@Attribute ADJ REAL', '@Attribute ADP REAL', '@Attribute ADV REAL',
                             '@Attribute AUX REAL', '@Attribute CCONJ REAL', '@Attribute DET REAL',
                             '@Attribute INTJ REAL', '@Attribute NOUN REAL', '@Attribute NUM REAL',
                             '@Attribute PART REAL', '@Attribute PRON REAL',
                             '@Attribute PROPN REAL', '@Attribute PUNCT REAL', '@Attribute SCONJ REAL',
                             '@Attribute SYM REAL', '@Attribute VERB REAL', '@Attribute X REAL']}
    return return_dict


def highlighted_words(inputtext):

    global sp

    if not "sp" in globals():
        sp = spacy.load("en_core_web_sm")

    splittext = sp(inputtext)

    preWord = ""
    prepreWord = ""
    total = 0
    for word in splittext:
        word = word.text
        if word == prepreWord:
            total += 1
        prepreWord = preWord
        preWord = word

    return_dict = {'values': [total], 'heads': ['@Attribute highlighted_words REAL']}
    return return_dict


def no_more_words(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if (word == "..."):
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute no_more_words REAL']}
    return return_dict


def would_counter(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if (word == "would"):
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute would_counter REAL']}
    return return_dict


def exclamation_mark_counter(inputText):
    splittext = inputText.split(" ")
    total = 0
    for word in splittext:
        if word == "!":
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute exclamation_mark_counter REAL']}
    return return_dict


def if_counter(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if (word == "if"):
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute if_counter REAL']}
    return return_dict


def unless_counter(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if (word == "would"):
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute unless_counter REAL']}
    return return_dict


def until_counter(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if (word == "would"):
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute until_counter REAL']}
    return return_dict