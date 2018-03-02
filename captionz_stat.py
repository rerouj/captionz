import csv

def write_csv(file_name):

    with open('{}.csv'.format(file_name), 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
    return filewriter


def uniq_word(corpus):

    uniq_word_list = list()
    for i in corpus:
        if i in uniq_word_list:
            pass
        else:
            uniq_word_list.append(i)
    return uniq_word_list


def count_word(corpus):

    counter = []
    #corpus_temp = corpus.split(' ')

    for word in corpus:
        counter.append(corpus.count(word))

    temp = list(zip(corpus, counter))

    word_count_dict = list()
    for i in temp:
        while i not in word_count_dict:
            word_count_dict.append(i)

    return word_count_dict

def freq_table(list_ready):

    if len(list_ready) < 10:
        len_tr = 1
        freq_table_ready = (len_tr, len(list_ready))
        return freq_table_ready

    elif len(list_ready) >9 and len(list_ready)<20:
        len_tr = 2
        freq_table_ready = (len_tr, len(list_ready)-1)
        return freq_table_ready

    elif len(list_ready) >19 and len(list_ready)<30:
        len_tr = 3
        freq_table_ready = (len_tr, len(list_ready)-1)
        return freq_table_ready

    elif len(list_ready) > 29 and len(list_ready) < 40:
        len_tr = 4
        freq_table_ready = (len_tr, len(list_ready)-1)
        return freq_table_ready

    elif len(list_ready) >39 and len(list_ready)<50:
        len_tr = 5
        freq_table_ready = (len_tr, len(list_ready)-1)
        return freq_table_ready

    elif len(list_ready) >49:
        len_tr = 5
        freq_table_ready = (len_tr, 50)
        return freq_table_ready


def getKey(item):
    return item[1]