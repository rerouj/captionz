# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, render_template, session
from captionz_nlp import *
from captionz_stat import *

import requests
import json

app = Flask(__name__)

# instagram app KEYS

app.secret_key = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""
connect_link = ""

about_text = 'Captionz is a little application for analyse your Instagram captions. ' \
             'The principle is very simple : the app takes all your captions,' \
             ' it extract a corpus and then process simple statistics analysis. ' \
             'The app separates words from emojis and from hashtags ' \
             'then it makes simple natural language processing on the different ' \
             'corpuses. Because emoji’s are complexe to extract, the analysis ' \
             'on the emoji corpus is not available for the moment. If you have ' \
             'other Instagram account, just logout and reload the captionz! ' \
             'main page. Please report bug at : info@tannhauser.ch'

stat_text = 'What about the numbers at the bottom ? 1) The first number shows the number ' \
            'of captions analysed. 2) The second shows the number of words used in your ' \
            'captions. 3) The third shows the number of unique word in the corpus. ' \
            '4) Finaly, the last one shows the number of hashtag in your captions. ' \
            'In the following section you will find the "word freq.(50)” section. ' \
            'These section is showing you the relative frequency (their occurency) ' \
            'of the words in your captions. Only, the 50 most popular word are displayed.'


@app.route('/')
def racine():
    return render_template('accueil.html',
                           titre='Captionz!',
                           about=about_text,
                           stat=stat_text,
                           link=connect_link,
                           legal='https://captionz.herokuapp.com/legal/privacy_policy')


@app.route('/token')
def get_token():

    code = request.args.get('code')
    response = requests.post("https://api.instagram.com/oauth/access_token",
                             data={'client_id': '15f83b5a8fee460f8fb975f780a336e2',
                                   'client_secret': '54d3457c7af9403da94ed7908c8cff26',
                                   'grant_type': 'authorization_code',
                                   'redirect_uri': 'https://captionz.herokuapp.com/token',
                                   'code': code})

    session['token'] = response.text

    return redirect('captionz')


''' get others captions on next pages '''


def pagination(page, captions_list):

    if bool(page['pagination']):
        next_page_url = page['pagination']['next_url']
        next_page_req = requests.get(str(next_page_url))
        next_page_parsed = json.loads(next_page_req.text)

        for i in range(len(next_page_parsed['data'])):
            try:
                captions_list.append([next_page_parsed['data'][i]['caption']['text']])
            except TypeError:
                captions_list.append(['empty'])

        pagination(next_page_parsed, captions_list)

    else:
        pass
    return captions_list


''' get captions and returns corpuses '''


def corpus_processor():

    token = session['token']
    captions = list()

    parsed = json.loads(token.encode('utf-8'))
    recent_media = requests.get(url='https://api.instagram.com/v1/users/self/media/'
                                    'recent/?access_token={}&count=32'.format(parsed['access_token']))
    recent_media_parsed = json.loads(recent_media.text)

    ''' Fill captions list with the first 32 results'''
    for i in range(len(recent_media_parsed['data'])):
        try:
            captions.append([recent_media_parsed['data'][i]['caption']['text']])
        except TypeError:
            captions.append(['empty'])

    ''' Get other captions on the following pages '''
    captions = pagination(recent_media_parsed, captions)

    '''Creating corpuses. Fonction on captionz_nlp.py'''

    raw_corpus = clean_emojis(captions, emoji_pattern1)
    corpus = caption_to_str(raw_corpus[0])
    corpus_cleaned = clean_special_char(corpus)
    hashtag_raw_list_test = extract_hashtags(corpus_cleaned)
    hashtag_list_stat_ready = list_hasthag(hashtag_raw_list_test)
    corpus_stat_ready = delete_hashtags(corpus_cleaned)
    corpus_stat_ready = corpus_stat_ready.split()

    return corpus_stat_ready, hashtag_list_stat_ready, captions


@app.route('/captionz')
def captionz():

    stat_ready = corpus_processor()
    # liste des mots (mots unique)
    uniq_word_list = uniq_word(stat_ready[0])
    # freq. des mots
    word_count = count_word(stat_ready[0])
    sorted_word_count = sorted(word_count, key=getKey, reverse=True)
    freq_table_return = freq_table(sorted_word_count)

    '''affichage sur le site'''

    return render_template('captionz.html',
                           titre='Captionz!',
                           titre1='Captions',
                           titre2='Words',
                           titre3='Unique',
                           titre4='#',
                           titre5='Word freq.(50)',
                           caption_num=len(stat_ready[2]),
                           len_words=len(stat_ready[0]),
                           len_uniq_words=len(uniq_word_list),
                           len_hashtags=len(stat_ready[1]),
                           word_freq=sorted_word_count,
                           freq_table=freq_table_return,
                           about=about_text,
                           stat=stat_text,
                           legal='https://captionz.herokuapp.com/legal/privacy_policy',
                           )


@app.route('/legal/privacy_policy')
def privacy():
    return render_template('privacy_policy.html',
                           titre='Captionz!',
                           about=about_text,
                           stat=stat_text,
                           link=connect_link,
                           legal='https://captionz.herokuapp.com/legal/privacy_policy')


if __name__ == '__main__':
    #app.run(debug=True)

    app.run(host='https://captionz.herokuapp.com', debug=False)
