import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from sklearn.model_selection import cross_val_score


def readDataset(path):
    print(f'Reading dataset {path}...')
    df = pd.read_csv(path, sep=';')
    text = df['tweet_text']
    label = df['sentiment']

    return text, label

def stem(corpus, stemmer):
    print(f'Stemming corpus...')

    corpusStem = []
    for sent in corpus:
        words = word_tokenize(sent)
        wordsStem = [stemmer.stem(word) for word in words]
        corpusStem.append(' '.join(wordsStem))
    return corpusStem


def vectorize(corpus):
    print(f'Vectorizing corpus...')
    tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('portuguese'))
    X = tfidfconverter.fit_transform(corpus).toarray()
    return X


def testModel(stemmer):


    text, labels = readDataset('archive/TrainingDatasets/Train100.csv')

    # textTest, labelsTest = readDataset('archive/TestDatasets/Test.csv')


    textStem = stem(text, stemmer)
    X = vectorize(textStem)

    # textTestStem = stem(textTest, stemmer)
    # XTest = vectorize(textTestStem)

    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import train_test_split

    # X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=0)
    # # X_train = X
    # # y_train = labels

    # # X_test = XTest
    # # y_test = labelsTest

    gnb = GaussianNB()
    # y_pred = gnb.fit(X_train, y_train).predict(X_test)

    scores = cross_val_score(gnb, X, labels, cv=10)

    print(scores)
    print(f'MEAN {np.array(scores).mean()}')
    print(f'STD {np.array(scores).std()}')
    # from sklearn import metrics

    # print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    # print('F1 macro', metrics.f1_score(y_test, y_pred, average='macro'))
    # print('F1 micro', metrics.f1_score(y_test, y_pred, average='micro'))


from nltk.stem import RSLPStemmer #http://www.inf.ufrgs.br/~viviane/rslp/index.htm removedor de sufixos lingua portuguesa
rslp = RSLPStemmer()

from nltk.stem.snowball import SnowballStemmer
snow = SnowballStemmer(language='portuguese')

testModel(rslp)
testModel(snow)