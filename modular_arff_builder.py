'''
Created on Oct 7, 2017

@author: dij
'''
import logging
import csv
import time
from features.length_feature import text_length
from features.length_feature import sentence_length
from features.words_features import bad_words
from features.words_features import positiv_negativ_words
from features.words_features import highlighted_words
from features.words_features import no_more_words
from features.words_features import would_counter

def main():
    
    base_path = "./generated/"
    logging.basicConfig(filename=base_path + 'log.log', level=logging.INFO)
    csv_value_index = 0
    csv_target_label_index = 1
    
    #data_file_path = "./data/hatespeech_task_train.csv"
    #data_file_path = "./data/spam_task_train.csv"
    data_file_path = "./data/sentiment_task_train.csv"
    
    features_csv_path = base_path + "features.csv"
    data_file_delimiter = "\t"
    omtArffName = "omt.arff"
    relationship_name = "@RELATION target"
    class_name = "@ATTRIBUTE TARGET {0, 1}"
        
    start = time.time()
    
    feature_functions = []

    #feature_functions.append(text_length)
    #feature_functions.append(sentence_length)
    #feature_functions.append(bad_words)
    feature_functions.append(positiv_negativ_words)
    #feature_functions.append(highlighted_words)
    #feature_functions.append(no_more_words)
    #feature_functions.append(would_counter)


    csv_reader = csv.reader(open(data_file_path, encoding="utf-8"), delimiter = data_file_delimiter)
    data_lines = [line for line in csv_reader]
    
    arff_lines = list()
        
    line_count = 1
    for line in data_lines:
        
        print(str(line_count) + "    von        " + str(len(data_lines)))
        logging.info('    verarbeite Line Nr ' + str(line_count) + '    in ModularArffBuilder')
        logging.info('    lines total in modularArffBuilder: ' + str(len(data_lines)))
        num_feature = 0
        for feature in feature_functions:
            num_feature += 1
            data_text = line[csv_value_index]

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
    
if __name__ == "__main__":
    main()