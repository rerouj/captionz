# -*- coding: utf-8 -*-
import re
import emoji

hashtag_final_list = list()

emoji_pattern1 = re.compile(u"[^\U00000000-\U0000d7ff\U0000e000-\U0000ffff]", flags=re.UNICODE)

'''préparation du corpus'''

# extracteur de hashtag. renvoie une liste
# de liste de hashtag correspondant aux phrases.
# il faut donc retraiter la liste avec


def extract_hashtags(text):
    regex = '#[a-z\w0-9\S]*'
    hashtag_list = re.findall(regex, text)
    return hashtag_list

# supprime les hashtags du corpus une
# fois que ces derniers ont été  extraits


def delete_hashtags(text):
    regex = '#[A-Za-z0-9]*'
    clean = re.sub(regex, '', text)
    return clean


def clean_special_char(text):
    special_char = '[\.\:\!\?\-\_\,\'\"\(\)\&\%\*\n]'
    clean = re.sub(special_char, ' ', text)
    return clean

# établi la liste finale des hashtags


def list_hasthag(hashtag_raw_list):

    hashtag_final_list = []
    for list_tag in hashtag_raw_list:
        temp = list_tag.split()
        for tag in temp:
            hashtag_final_list.append(tag)
    return hashtag_final_list


def caption_to_str(caption_list):
    corpus = str()
    for i in range(len(caption_list)):
        if caption_list[i][0] == 'empty':
            pass
        else:
            cap = caption_list[i][0]
            corpus = corpus+'{}\n\n'.format(cap)
    return corpus


'''sortie fichiers'''


def raw_text_corpus(text):
    with open('raw_clean.txt', 'w') as clean:
        clean.write(text)
    clean.close()


def hashtag_str_list(hashtag_list):
    hashtag_corpus_str = str()
    for i in hashtag_list:
        hashtag_corpus_str = hashtag_corpus_str+'{} '.format(i)
    return hashtag_corpus_str


def hashtag_corpus(hashtag_list):
    with open('hashtag_corpus.txt', 'w') as hashtag_corpus_temp:
        hashtag_corpus_temp.write(hashtag_list)
    hashtag_corpus_temp.close()


def clean_emojis(raw_text, pattern):
    emoji_list = list()
    clean_text = list()
    for captions_in_raw_text in raw_text:
        #print(type(captions_in_raw_text[0]))
        emoji_temp_list = re.findall(pattern, captions_in_raw_text[0])
        emoji_list.append(emoji_temp_list)

        #temp = emoji_utils.remove_emoji(captions_in_raw_text[0])
        temp = emoji_pattern1.sub(r'', captions_in_raw_text[0])

        #print([temp])
        clean_text.append([temp])
    return clean_text, emoji_list
