import csv
import re


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
    splittext = inputtext.split(" ")
    total = 0

    positiv = 0
    negativ = 0

    data_file_path = "C:/Users/U725803/Documents/Super_duper_ki/data/SentiWords_1.1.txt"

    f = open(data_file_path, "r")
    data_lines = f.readlines()
    for line in data_lines:
        splitline = line.split("#")
        words = splitline[0].split("_")
        if len(re.split(r'\t+', splitline[1])) >= 2:
            pos = re.split(r'\t+', splitline[1])[0]  # Part of speech
            score = float(re.split(r'\t+', splitline[1])[1].replace("\n", ""))
            for j in range(len(splittext)):
                matches = 0
                for i in range(len(words)):
                    if words[i] == splittext[j]:
                        matches += 1
                if matches == len(words) and len(words) > 0:
                    total += score
                    if score > 0:
                        positiv += score
                    else:
                        negativ += score

    f.close()

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
