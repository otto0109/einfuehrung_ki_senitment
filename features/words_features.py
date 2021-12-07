import csv
import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

basePath = "C:/Users/PC/DevProjects/Uni/"
pos_words_dir = basePath + "Super_duper_ki/data/positive-words.txt"
neg_words_dir = basePath + "Super_duper_ki/data/negative-words.txt"
analyzer = SentimentIntensityAnalyzer()

def analyse_sentence_score(inputtext):
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

def bad_words(inputtext):
    data_file_delimiter = "\t"
    data_file_path = basePath + "Super_duper_ki/data/bad_word_list.csv"
    splittext = inputtext.split(" ")
    total = 0
    csv_reader = csv.reader(open(data_file_path, encoding="utf-8"), delimiter=data_file_delimiter)
    data_lines = [line for line in csv_reader]
    for word in splittext:
        if (len(word) > 0):
            for line in data_lines:
                if (word in line):
                    total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute bad_words REAL']}
    return return_dict


def positiv_negativ_words(inputtext):

    global data_lines
    global sentimented_words
    global sentimented_pos
    global sentimented_score
    global sp

    total = 0
    positiv = 0
    negativ = 0

    if not "sp" in globals():
        sp = spacy.load("en_core_web_sm")
    if not "data_lines" in globals():
        data_file_path = basePath + "Super_duper_ki/data/SentiWords_1.1.txt"
        f = open(data_file_path, "r")
        data_lines = f.readlines()
        sentimented_words = []
        sentimented_pos = []
        sentimented_score = []
        for line in data_lines:
            splitline = line.split("#")
            words = splitline[0].replace("_", " ")
            if len(re.split(r'\t+', splitline[1])) >= 2:
                pos = re.split(r'\t+', splitline[1])[0]  # Part of speech
                score = float(re.split(r'\t+', splitline[1])[1].replace("\n", ""))
                sentimented_words.append(words)
                sentimented_pos.append(pos)
                sentimented_score.append(score)
        f.close()

    sen = sp(inputtext)

    for token in sen:
        if len(token.text) > 0:
            try:
                index = sentimented_words.index(token.text)
                word = token.text
                if index < 0:
                    sentimented_words.index(token.lemma_)
                    word = token.lemma_

                score = sentimented_score[index]
                pos = sentimented_pos[index]
                spacyPos = "n" if token.pos_ == "NOUN" else "a" if token.pos_ == "ADJ" else "v" if token.pos_ == "VERB" else token.pos_

                if sentimented_words[index] == word:
                    if pos == spacyPos:
                        total += score
                        if score > 0:
                            positiv += score
                        else:
                            negativ += score
            except:
                index = 0

    return_dict = {'values': [total, total / len(sen), positiv / len(sen), negativ / len(sen)],
                   'heads': ['@Attribute positiv_negativ_words REAL',
                             '@Attribute positiv_negativ_words_ratio REAL',
                             '@Attribute negativ_words_ratio REAL',
                             '@Attribute positiv_words_ratio REAL']}

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


def neg_pos_words_ratio(inputtext):
    global sp
    global pos_words_lines
    global neg_words_lines


    if not "sp" in globals():
        sp = spacy.load("en_core_web_sm")

    if not "pos_words_lines" in globals():
        pos_words_lines = []
        with open(pos_words_dir) as pos_file:
            pos_words_lines = pos_file.readlines()
            pos_words_lines = [i.replace("\n", "") for i in pos_words_lines]

    if not "neg_words_lines" in globals():
        neg_words_lines = []
        with open(neg_words_dir) as neg_file:
            neg_words_lines = neg_file.readlines()
            neg_words_lines = [i.replace("\n", "") for i in neg_words_lines]

    splittext = sp(inputtext)

    total_pos = 0
    total_neg = 0

    for token in splittext:
        word = token.text
        if len(word) > 0:
            try:
                index = pos_words_lines.index(word)
                word2 = pos_words_lines[index]
                if word2 == word:
                    total_pos += 1
                else:
                    word = token.lemma_
                    index = pos_words_lines.index(word)
                    word2 = pos_words_lines[index]
                    if word2 == word:
                        total_pos += 1
            except:
                index = 0
            try:
                index = neg_words_lines.index(word)
                word2 = neg_words_lines[index]
                if word2 == word:
                    total_neg += 1
                else:
                    word = token.lemma_
                    index = pos_words_lines.index(word)
                    word2 = pos_words_lines[index]
                    if word2 == word:
                        total_neg += 1
            except:
                index = 0

    total_neg_words = float(total_neg)
    total_pos_words = float(total_pos)
    amount_total_words = float(len(splittext))

    return_dict = {'values': [total_pos_words / amount_total_words, total_neg_words / amount_total_words],
                   'heads': ['@Attribute pos_words_ratio REAL', '@Attribute neg_words_ratio REAL']}

    return return_dict


def exclamation_mark_counter(inputText):
    splittext = inputText.split(" ")
    total = 0
    for word in splittext:
        if word == "!":
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute exclamation_mark_counter REAL']}
    return return_dict

def not_counter(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if (word == "not" or word == "n't" or word == "'t"):
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute not_counter REAL']}
    return return_dict