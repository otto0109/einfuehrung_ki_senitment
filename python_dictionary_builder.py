from csv import reader
import spacy
from features.grammer_features import fix_grammer
import time
import os.path
import io


def main():
    data_file_delimiter = "\t"
    data_file_path = "./data/sentiment_task_train.csv"
    csv_reader = reader(open(data_file_path, encoding="utf-8"), delimiter=data_file_delimiter)
    data_lines = [line for line in csv_reader]
    sp = spacy.load("en_core_web_sm")
    grammer_cache_path = "grammer_cache.txt"

    positiv_words = {

    }

    negativ_words = {

    }

    words = {

    }

    overall_use = {

    }

    start = time.time()

    line_count = 1

    fixed_grammer = []

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

    cache_write = ""

    for line in data_lines:
        end = time.time()
        printProgressBar(line_count, len(data_lines), prefix='Progress:', suffix='Complete', length=100, time=str(int(end - start)) + "sec")

        data_text = line[0]
        sentiment_type = line[1]

        if len(fixed_grammer) == 0:
            data_text, debug_text = fix_grammer(data_text)
            cache_write += data_text + "\n"
        else:
            data_text = fixed_grammer[line_count - 1]

        sen = sp(data_text)

        for token in sen:
            if token.lemma_ in overall_use:
                overall_use[token.lemma_] = overall_use[token.lemma_] + 1
            else:
                overall_use[token.lemma_] = 1
            if sentiment_type == "0":
                if token.lemma_ in negativ_words:
                    negativ_words[token.lemma_] = negativ_words[token.lemma_] + 1
                else:
                    negativ_words[token.lemma_] = 1
                if token.lemma_ in words:
                    words[token.lemma_] = words[token.lemma_] - 1
                else:
                    words[token.lemma_] = -1
            else:
                if token.lemma_ in positiv_words:
                    positiv_words[token.lemma_] = positiv_words[token.lemma_] + 1
                else:
                    positiv_words[token.lemma_] = 1
                if token.lemma_ in words:
                    words[token.lemma_] = words[token.lemma_] + 1
                else:
                    words[token.lemma_] = 1
        line_count += 1

    with io.open(grammer_cache_path, 'a', encoding='utf8') as f:
        f.write(cache_write)
        f.close()

    fi = open("words.txt", "w")
    fi.close()

    print("====================================== Overview of words in document ======================================")
    for key in words:
        overall_count = overall_use[key]
        if words[key] < 0:
            score = (negativ_words[key] * -1)
            negative_count = score * -1
            positive_count = overall_count - negative_count
        else:
            score = positiv_words[key]
            positive_count = score
            negative_count = overall_count - positive_count
        print(key + ": POS: " + str(positive_count) + "; NEG: " + str(negative_count) + "; OVERALL: " + str(overall_count))
        words[key] = score / overall_count

    words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))

    with io.open("words.txt", 'a', encoding='utf8') as file:
        for key in words:
            if overall_use[key] > 10:
                file.write(key + " " + str(words[key]) + "\n")
        file.close()
    print("Finished. File was successfully generated.")


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

