import re
from datetime import datetime

from bs4 import BeautifulSoup
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

import env
from constants import EXTENSION_TFIDF, DIR_TFIDF
from file_manager import dump_file

time = datetime.now().strftime("%d%b%Y%H%M%S")
processed = 0
tok = WordPunctTokenizer()
lem = WordNetLemmatizer()


def text_processing(tweet):
    tweet = BeautifulSoup(tweet, 'lxml').get_text() # HTML elemek dekódolása
    tweet = tweet.lower()
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet) # @ mention-ök szűrése
    tweet = re.sub('https?://[A-Za-z0-9./]+','', tweet) # linkek szűrése
    tweet = tweet.encode('utf-8-sig').decode("utf-8-sig")
    tweet = re.sub("[^a-zA-Z]", " ", tweet) # hashmarkok és számok szűrése
    if env.STOPWORDS:
        tweet = [t for t in tweet.split() if re.match(r'[^\W\d]*$', t)]
    tweet = tok.tokenize(tweet) # tokenizálás
    if env.STOPWORDS:
        tweet = [word for word in tweet if word not in stopwords.words('english')] # ---------> stopword-ök szűrése
    tweet = [lem.lemmatize(word, 'v') for word in tweet] # szavak normalizálása

    # Meghosszabbított szavak lerövidítése, pl "awesoooome"
    def replace_elongated_words(tweet_list):

        def replace_elongated_word(word):
            regex = r'(\w*)(\w+)\2(\w*)'
            repl = r'\1\2\3'
            if wordnet.synsets(word):
                return word
            new_word = re.sub(regex, repl, word)
            if new_word != word:
                return replace_elongated_word(new_word)
            else:
                return new_word

        shortened_tweet = []
        for word in tweet_list:
            shortened_text = replace_elongated_word(word)
            shortened_tweet.append(shortened_text)

        return shortened_tweet

    tweet = replace_elongated_words(tweet)

    global processed
    processed += 1
    if processed % 2000 == 0:
        print(processed / 2, 'records processed')

    return tweet


def vectorize_tweets(model, dataset, features):
    tfidf = TfidfVectorizer(max_features=features, analyzer=text_processing)
    tfidf = tfidf.fit(dataset)

    dump_file(tfidf, 'tfidf', DIR_TFIDF, model, EXTENSION_TFIDF)

    return tfidf


def transform_tfidf(tfidf, dataset):
    return tfidf.transform(dataset).toarray()
