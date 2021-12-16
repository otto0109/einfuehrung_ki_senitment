'''
Created on Oct 7, 2017

@author: dij
'''
import logging
import csv
import time
import os.path
import io
from features.length_feature import text_length
from features.length_feature import sentence_length
from features.lexicon_features import bad_words
from features.lexicon_features import senti_words
from features.words_features import highlighted_words
from features.words_features import no_more_words
from features.words_features import would_counter
from features.lexicon_features import simple_lexikon
from features.words_features import exclamation_mark_counter
from features.lexicon_features import negation_counter
from features.words_features import part_of_speech
from features.words_features import analyse_sentence_score
from features.grammer_features import fix_grammer
from features.grammer_features import bad_grammer
from features.lexicon_features import afinn
from features.lexicon_features import senti_word_net
from features.lexicon_features import own_lexikon

def main():
    
    base_path = "./generated/"
    base_path_test = "./generated/test/"

    logging.basicConfig(filename=base_path + 'log.log', level=logging.INFO)

    #data_file_path = "./data/hatespeech_task_train.csv"
    #data_file_path = "./data/spam_task_train.csv"
    data_file_path = "./data/sentiment_task_train.csv"
    data_file_path_test = "./data/sentiment_task_test.csv"
    debug_grammer_path = base_path + "depugGrammer.txt"
    debug_grammer_path_test = base_path + "depugGrammer_test.txt"
    grammer_cache_path = "grammer_cache.txt"
    grammer_cache_path_test = "grammer_cache_test.txt"

        
    feature_functions = []

    #feature_functions.append(bad_grammer)
    #feature_functions.append(text_length)
    #feature_functions.append(sentence_length)
    #feature_functions.append(bad_words)
    feature_functions.append(senti_words)
    #feature_functions.append(highlighted_words)
    #feature_functions.append(no_more_words)
    feature_functions.append(would_counter)
    feature_functions.append(simple_lexikon)
    #feature_functions.append(exclamation_mark_counter)
    #feature_functions.append(negation_counter)
    #feature_functions.append(part_of_speech)
    feature_functions.append(analyse_sentence_score)
    #feature_functions.append(afinn)
    feature_functions.append(senti_word_net)
    feature_functions.append(own_lexikon)

    print("generate Train arff\n")

    generateArff(base_path, data_file_path, feature_functions, debug_grammer_path, grammer_cache_path)

    print("generate Test arff\n")

    generateArff(base_path_test, data_file_path_test,feature_functions, debug_grammer_path_test, grammer_cache_path_test)


def generateArff(base_path, data_file_path, feature_functions, debug_grammer_path, grammer_cache_path):

    csv_value_index = 0
    csv_target_label_index = 1

    start = time.time()
    features_csv_path = base_path + "features.csv"
    data_file_delimiter = "\t"
    omtArffName = "omt.arff"
    relationship_name = "@RELATION target"
    class_name = "@ATTRIBUTE TARGET {0, 1}"

    csv_reader = csv.reader(open(data_file_path, encoding="utf-8"), delimiter=data_file_delimiter)
    data_lines = [line for line in csv_reader]
    arff_lines = list()

    f = open(debug_grammer_path, "w")
    f.write("")
    f.close()

    if os.path.isfile(grammer_cache_path):
        fixed_grammer = [line.rstrip() for line in open(grammer_cache_path)]
        if len(fixed_grammer) == 0:
            fixed_grammer = []
            fi = open(grammer_cache_path, "w")
            fi.write("")
            fi.close()
    else:
        fi = open(grammer_cache_path, "w")
        fi.close()

    line_count = 1

    cache_write = ""
    debug_write = ""

    for line in data_lines:
        end = time.time()
        printProgressBar(line_count, len(data_lines), prefix='Progress:', suffix='Complete', length=100, time=str(int(end - start)) + "sec")
        logging.info('    verarbeite Line Nr ' + str(line_count) + '    in ModularArffBuilder')
        logging.info('    lines total in modularArffBuilder: ' + str(len(data_lines)))
        num_feature = 0
        data_text = line[csv_value_index]
        for feature in feature_functions:

            num_feature += 1

            if num_feature == 1 and len(fixed_grammer) != len(data_lines):
                data_text, debug_text = fix_grammer(data_text)
                cache_write += data_text + "\n"
                debug_write += debug_text
            else:
                if num_feature == 1:
                    data_text = fixed_grammer[line_count - 1]

            result_dict = feature(data_text)

            values = result_dict.get('values')
            heads = result_dict.get('heads')

            head_flag = False

            value_counter = 0
            for head in heads:
                if len(arff_lines) == 0:                        # arff_lines has just been newly created
                    arff_lines.append([head])
                    arff_lines.append([values[value_counter]])    # first head arff_lines[0] and first value arff_lines[1] added
                    head_flag = True
                else:
                    if not head in arff_lines[0]:
                        arff_lines[0].append(head)                                    #feature has not yet been written in csv - append to head
                        arff_lines[line_count].append(values[value_counter])        # since a new index needs to be added, also add value to the end
                        head_flag = True
                    else:
                        if (len(arff_lines) - 1) < line_count:
                            arff_lines.append([values[value_counter]])                # add new line to the end of arff_lines
                        else:
                            if (len(arff_lines[line_count]) - 1) < arff_lines[0].index(head):
                                arff_lines[line_count].append(values[value_counter])    # if head-index extends line indices, append.
                            else:
                                arff_lines[line_count][arff_lines[0].index(head)] = values[value_counter]    #fill the current line with values per head
                value_counter += 1

            if not head_flag:
                value_to_add = line[csv_target_label_index]
                arff_lines[line_count].append(value_to_add)
            else:
                if num_feature == len(feature_functions):
                    value_to_add = line[csv_target_label_index]
                    arff_lines[line_count].append(value_to_add)

        line_count += 1

    with io.open(grammer_cache_path, 'a', encoding='utf8') as f:
        f.write(cache_write)
        f.close()

    with io.open(debug_grammer_path, 'a', encoding='utf8') as file:
        file.write(debug_write)
        file.close()

    if not class_name in arff_lines[0]:
        class_name = class_name.replace("'", "")
        class_name = class_name.replace(",", "")
        arff_lines[0].extend([class_name])

    with open(features_csv_path, 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar="'", quoting=csv.QUOTE_NONE, escapechar='\\')
        for line in arff_lines:
            writer.writerow(line)

    # now that the csv is done, we need to build the .arff file
    reader = csv.reader(open(features_csv_path))
    arff_lines = [line for line in reader]

    with open(base_path + omtArffName, "w") as arff:
        arff.write(relationship_name + "\n")
        for feature_head in arff_lines[0]:
            feature_head = feature_head.replace('[','{')
            feature_head = feature_head.replace(']','}')
            arff.write(feature_head.lstrip() + "\n")
        arff.write("@DATA\n")

    # leave out the first (head) line and write each line, separated by commas
        count_line = 0;
        for line_to_write in arff_lines:
            if count_line > 0:
                count_word = 0
                for word in line_to_write:
                    arff.write(word)
                    if (count_word + 1) < len(line_to_write):
                        arff.write(", ")
                    count_word += 1
                arff.write("\n")
            count_line += 1

    # monitor time taken to compute
    end = time.time()
    print(end - start)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', autosize = False, time = ""):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resJize the length of the progress bar to the terminal window (Bool)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s %s' % (prefix, fill, percent, suffix, "time:" + time)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback = (length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

if __name__ == "__main__":
    main()