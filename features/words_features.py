import csv
import re
import spacy

pos_words_dir = "C:/Users/PC/PycharmProjects/Super_duper_ki/data/positive-words.txt"
neg_words_dir = "C:/Users/PC/PycharmProjects/Super_duper_ki/data/negative-words.txt"


def bad_words(inputtext):
    data_file_delimiter = "\t"
    data_file_path = "C:/Users/U725803/Documents/Super_duper_ki/data/bad_word_list.csv"
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

    sp = spacy.load("en_core_web_sm")
    sen = sp(inputtext)

    total = 0

    positiv = 0
    negativ = 0

    if not "data_lines" in globals():
        data_file_path = "C:/Users/PC/PycharmProjects/Super_duper_ki/data/SentiWords_1.1.txt"
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

    for word in splittext:
        if len(word) > 0:
            try:
                index = sentimented_words.index(word)
                score = sentimented_score[index]
                if sentimented_words[index] == word:
                    total += score
                    if score > 0:
                        positiv += score
                    else:
                        negativ += score
            except:
                index = 0
    if "no" in splittext:
        total *= -1
        positiv *= -1
        negativ *= -1

    return_dict = {'values': [total, total / len(splittext), positiv / len(splittext), negativ / len(splittext)],
                   'heads': ['@Attribute positiv_negativ_words REAL',
                             '@Attribute positiv_negativ_words_ratio REAL',
                             '@Attribute negativ_words_ratio REAL',
                             '@Attribute positiv_words_ratio REAL']}

    return return_dict


def highlighted_words(inputtext):
    splittext = inputtext.split(" ")
    preWord = ""
    prepreWord = ""
    total = 0
    for word in splittext:
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
    pos_words_lines = []
    neg_words_lines = []

    with open(pos_words_dir) as pos_file:
        pos_words_lines = pos_file.readlines()
        pos_words_lines = [i.replace("\n", "") for i in pos_words_lines]

    with open(neg_words_dir) as neg_file:
        neg_words_lines = neg_file.readlines()
        neg_words_lines = [i.replace("\n", "") for i in neg_words_lines]

    splittext = inputtext.split(" ")

    total_pos = 0
    total_neg = 0

    for word in splittext:
        if len(word) > 0:
            try:
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
            except:
                index = 0

    if "no" in splittext:
        store = total_neg
        total_neg = total_pos
        total_pos = store

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