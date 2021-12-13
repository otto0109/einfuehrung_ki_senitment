import csv
import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import language_tool_python
import io
from afinn import Afinn
from nltk.corpus import sentiwordnet as swnb
from pywsd.lesk import simple_lesk
import nltk

nltk.download('sentiwordnet')
basePath = "C:/Users/thorg/IdeaProjects/"
pos_words_dir = basePath + "Super_duper_ki/data/positive-words.txt"
neg_words_dir = basePath + "Super_duper_ki/data/negative-words.txt"
#Quelle: https://stackoverflow.com/questions/43018030/replace-apostrophe-short-words-in-python
contractions = {
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'd've": "he would have",
"he'll": "he shall",
"he'll've": "he shall have",
"he's": "he has",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has",
"i'd": "I had",
"i'd've": "I would have",
"i'll": "I shall",
"i'll've": "I shall have",
"i'm": "I am",
"i've": "I have",
"isn't": "is not",
"it'd": "it had",
"it'd've": "it would have",
"it'll": "it shall",
"it'll've": "it shall have",
"it's": "it has",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had",
"she'd've": "she would have",
"she'll": "she shall",
"she'll've": "she shall have",
"she's": "she has",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that has",
"there'd": "there had",
"there'd've": "there would have",
"there's": "there has",
"they'd": "they had",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}
def fix_grammer(inputtext):
    global tool

    if not "tool" in globals():
        tool = language_tool_python.LanguageTool('en-US')


    text = inputtext

    with io.open("depugGrammer.txt", 'a', encoding='utf8') as f:
        f.write(text)
        f.write("\n")
    text = tool.correct(text)
    text = text.replace(" 't", "'t")
    for word in text.split():
        if word.lower() in contractions:
            text = text.replace(word, contractions[word.lower()])
    text = tool.correct(text)
    text = text.lower()
    with io.open("depugGrammer.txt", 'a', encoding='utf8') as f:
            f.write(text)
            f.write("\n")
            f.write("\n")

    f.close()
    return text

def bad_grammer(inputtext):
    global tool

    if not "tool" in globals():
        tool = language_tool_python.LanguageTool('en-US')

    text = inputtext
    matches = tool.check(text)
    matches = [rule for rule in matches if not is_bad_rule(rule)]
    return_dict = {
        'values': [ len(text)/(len(matches) + 1) ],
        'heads': ['@Attribute bad_grammer_ratio REAL']}
    return return_dict

def is_bad_rule(rule):
    if rule.ruleId == "UPPERCASE_SENTENCE_START":
        return True

    if rule.ruleId == "I_LOWERCASE":
        return True

    return False

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

def score_pos_neg(inputtext):
    global sp

    total = 0
    positiv = 0
    negativ = 0
    gefundeneWörter = 1

    if not "sp" in globals():
        sp = spacy.load("en_core_web_sm")

    sen = sp(inputtext)

    for token in sen:
        spacyPos = "n" if token.pos_ == "NOUN" else "a" if token.pos_ == "ADJ" else "v" if token.pos_ == "VERB" else "skip"

        if spacyPos != "skip":
            try:
                answer = str(simple_lesk(inputtext, token.text, pos=spacyPos))
                answer = answer[8:len(answer)-2]
                score = swnb.senti_synset(answer)
                if score is not None and score.obj_score() != 1:
                    gefundeneWörter = gefundeneWörter + 1
                    total = total + float(score.obj_score())
                    positiv = positiv + float(score.pos_score())
                    negativ = negativ + float(score.neg_score())
            except:
                index = 0
    return_dict = {'values': [total, total / gefundeneWörter, negativ / gefundeneWörter, positiv / gefundeneWörter],
                       'heads': ['@Attribute positiv_negativ_words_swn REAL',
                                 '@Attribute positiv_negativ_words_swn_ratio REAL',
                                 '@Attribute negativ_words_swn_ratio REAL',
                                 '@Attribute positiv_words_swn_ratio REAL']}

    return return_dict


def afinn(inputtext):

    afinn = Afinn(language='en')

    score = afinn.score(inputtext)

    return_dict = {
        'values': [score],
        'heads': ['@Attribute afinn_score REAL',]}
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
        if ("not" in word or "n't" in word or "'t" in word):
            total += 1

    return_dict = {'values': [total], 'heads': ['@Attribute not_counter REAL']}
    return return_dict