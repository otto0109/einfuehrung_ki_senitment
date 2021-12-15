import io
import csv
import re
import spacy
import nltk
from nltk.corpus import sentiwordnet as swnb
from pywsd.lesk import simple_lesk
from afinn import Afinn

nltk.download('sentiwordnet')
basePath = "C:/Users/thorg/IdeaProjects/"
pos_words_dir = basePath + "Super_duper_ki/data/positive-words.txt"
neg_words_dir = basePath + "Super_duper_ki/data/negative-words.txt"


def senti_word_net(inputtext):
    global sp

    total = 0
    positiv = 0
    negativ = 0
    gefundeneWörter = 1

    if not "sp" in globals():
        sp = spacy.load("en_core_web_sm")

    sen = sp(inputtext)

    word_num = -1
    negation_words = negation(inputtext)

    for token in sen:
        word_num = word_num + 1
        spacyPos = "n" if token.pos_ == "NOUN" else "a" if token.pos_ == "ADJ" else "v" if token.pos_ == "VERB" else "skip"
        if spacyPos != "skip":
            try:
                answer = str(simple_lesk(inputtext, token.text, pos=spacyPos))
                answer = answer[8:len(answer) - 2]
                score = swnb.senti_synset(answer)
                if score is not None and score.obj_score() != 1:
                    gefundeneWörter = gefundeneWörter + 1
                    if negate_word_score(word_num, negation_words):
                        total = total + float(score.obj_score())
                        positiv = positiv + float(score.neg_score())
                        negativ = negativ + float(score.pos_score())
                    else:
                        total = total + float(score.obj_score())
                        positiv = positiv + float(score.pos_score())
                        negativ = negativ + float(score.neg_score())
            except:
                index = 0

    senti_type = 0 if positiv <= negativ else 1

    return_dict = {'values': [total, total / gefundeneWörter, negativ / gefundeneWörter, positiv / gefundeneWörter, senti_type],
               'heads': ['@Attribute positiv_negativ_words_swn REAL',
                         '@Attribute positiv_negativ_words_swn_ratio REAL',
                         '@Attribute negativ_words_swn_ratio REAL',
                         '@Attribute positiv_words_swn_ratio REAL',
                         '@Attribute decision_swn REAL']}

    return return_dict


def afinn(inputtext):
    afinn = Afinn(language='en')

    score = afinn.score(inputtext)

    return_dict = {
        'values': [score],
        'heads': ['@Attribute afinn_score REAL', ]}
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


def senti_words(inputtext):
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

    word_num = -1
    negation_words = negation(inputtext)

    for token in sen:
        if len(token.text) > 0:
            word_num = word_num + 1
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
                        if negate_word_score(word_num, negation_words):
                            score = score * -1
                        total += score
                        if score > 0:
                            positiv += score
                        else:
                            negativ += score
            except:
                index = 0

    senti_type = 0 if positiv <= negativ else 1

    return_dict = {'values': [total, total / len(sen), positiv / len(sen), negativ / len(sen), senti_type],
                   'heads': ['@Attribute senti_words_positiv_negativ_words REAL',
                             '@Attribute senti_words_positiv_negativ_words_ratio REAL',
                             '@Attribute senti_words_negativ_words_ratio REAL',
                             '@Attribute senti_words_positiv_words_ratio REAL',
                             '@Attribute senti_words_decision REAL']}

    return return_dict


def simple_lexikon(inputtext):
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

    word_num = -1
    negation_words = negation(inputtext)

    for token in splittext:
        word = token.text
        if len(word) > 0:
            word_num = word_num + 1
            try:
                index = pos_words_lines.index(word)
                word2 = pos_words_lines[index]
                if word2 == word:
                    if negate_word_score(word_num, negation_words):
                        total_neg += 1
                    total_pos += 1
                else:
                    word = token.lemma_
                    index = pos_words_lines.index(word)
                    word2 = pos_words_lines[index]
                    if word2 == word:
                        if negate_word_score(word_num, negation_words):
                            total_neg += 1
                        total_pos += 1
            except:
                index = 0
            try:
                index = neg_words_lines.index(word)
                word2 = neg_words_lines[index]
                if word2 == word:
                    if negate_word_score(word_num, negation_words):
                        total_pos += 1
                    total_neg += 1
                else:
                    word = token.lemma_
                    index = pos_words_lines.index(word)
                    word2 = pos_words_lines[index]
                    if word2 == word:
                        if negate_word_score(word_num, negation_words):
                            total_pos += 1
                        total_neg += 1
            except:
                index = 0

    total_neg_words = float(total_neg)
    total_pos_words = float(total_pos)
    amount_total_words = float(len(splittext))

    senti_type = 0 if total_pos_words <= total_neg_words else 1

    return_dict = {'values': [total_pos_words / amount_total_words, total_neg_words / amount_total_words, senti_type],
                   'heads': ['@Attribute simple_lexikon_pos_ratio REAL',
                             '@Attribute simple_lexikon_neg_ratio REAL',
                             '@Attribute simple_lexikon_decision REAL']}

    return return_dict


def negation_counter(inputtext):

    total = 0

    negation_words = ["no", "not", "none", "nobody", "nothing", "neither", "nowhere", "never"]

    words = inputtext.split(" ")

    for word in negation_words:
        for x in range(len(words)):
            if word == words[x]:
                total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute negation_counter REAL']}
    return return_dict


def negation(inputtext):
    senti_negation = []
    negation_words = ["no", "not", "none", "nobody", "nothing", "neither", "nowhere", "never"]

    words = inputtext.split(" ")

    for word in negation_words:
        for x in range(len(words)):
            if word == words[x]:
                senti_negation.append([word, x])


def negate_word_score(word_index, negation_words):
    for negation_word in negation_word:
        if negation_word[1] != word_index:
            if negation_word - word_index > -3 and negation_word - word_index < 3:
                return True

    return False
