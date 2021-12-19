def amount_cap_words(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    first = ""
    for word in splittext:
        if (len(word) > 0):
            first = word[0]
            if first.isupper():
                total += 1
    return_dict = {'values': [total], 'heads': ['@Attribute amount_cap_words REAL']}
    return return_dict


def links(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if ("<a" in word):
            total += 1
    return_dict = {'values': [total], 'heads': ['@Attribute amount_links REAL']}
    return return_dict


def is_response(inputtext):
    respo = 0
    if (inputtext.lower().startswith('re')):
        respo += 1
    return_dict = {'values': [respo], 'heads': ['@Attribute amount_response REAL']}
    return return_dict


def sale(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    for word in splittext:
        if ("sale" in word.lower()):
            total += 1
    return_dict = {'values': [total], 'heads': ['@Attribute amount_sale REAL']}
    return return_dict


def cap_word_ratio(inputtext):
    splittext = inputtext.split(" ")
    total = 0
    first = ""
    for word in splittext:
        if (len(word) > 0):
            first = word[0]
            if first.isupper():
                total += 1
    total_cap_words = float(total)
    amount_words = float(len(splittext))

    return_dict = {'values': [total_cap_words / amount_words], 'heads': ['@Attribute cap_word_ratio REAL']}
    return return_dict
