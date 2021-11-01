def text_length(inputtext):
    return_dict = {'values': [len(inputtext)], 'heads': ['@Attribute text_length REAL']}
    return return_dict

def sentence_length(inputtext):
    splittext = inputtext.split(".")
    total = 0
    for sentence in splittext:
            total += len(sentence)
    return_dict = {'values': [total / float(len(splittext))], 'heads': ['@Attribute sentence_length REAL']}
    return return_dict