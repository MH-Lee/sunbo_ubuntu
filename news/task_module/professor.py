import ast
import multiprocessing
import pickle
import pandas as pd
import numpy as np
import joblib
import re
import os
from collections import namedtuple
from sklearn.model_selection import train_test_split
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import konlpy
from konlpy.tag import Kkma, Okt, Hannanum, Twitter
from datetime import datetime
#tokenize & word2vec packages
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
from soynlp.noun import NewsNounExtractor
from gensim.models import Word2Vec
import gensim, logging
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.summarization import keywords
from newspaper import Article
from newspaper import fulltext
from news.task_module.news_crawler import NaverNewsCrawler
import platform
import os
# from news.task_module.professor import ProfessorNews

class ProfessorNews:
    def __init__(self):
        path = os.getcwd()
        # self.new_small = pd.read_excel('./nlp_data/new_small_class.xlsx')
        if platform.system() == 'Linux':
            # path = '/home/ubuntu/sunbo_django/recommender/models/'
            # path2 = '/home/ubuntu/sunbo_django/news/task_module'
            self.ko_stopwords = pd.read_csv(path + '/news/task_module/nlp_data/korean_stopwords.txt')
            self.token_stops = pd.read_csv(path + '/news/task_module/nlp_data/token_stopwords.csv', engine='python', encoding='cp949')['stopwords'].tolist()
            self.doc_vectorizer = Doc2Vec.load(path + '/recommender/models/Doc2vec1.model')
            self.doc_set = pd.read_excel(path + '/news/task_module/nlp_data/doc_set.xlsx')
            self.mlp_clf = joblib.load(path + '/news/task_module/nlp_material/mlp_clf.sav')
            self.mlp_clf2 = joblib.load(path + '/news/task_module/nlp_material/mlp_clf2.sav')
            if os.path.exists(path + '/news/task_module/backup_data/') == False:
                os.mkdir(path + '/news/task_module/backup_data/')
        else:
            self.ko_stopwords = pd.read_csv(path + '\\news\\task_module\\nlp_data\\korean_stopwords.txt')
            self.token_stops = pd.read_csv(path + '\\news\\task_module\\nlp_data\\token_stopwords.csv', engine='python', encoding='cp949')['stopwords'].tolist()
            self.doc_vectorizer = Doc2Vec.load(path + '\\recommender\\models\\Doc2vec1.model')
            self.doc_set = pd.read_excel(path + '\\news\\task_module\\nlp_data\\doc_set.xlsx')
            self.mlp_clf = joblib.load(path + '\\news\\task_module\\nlp_material\\mlp_clf.sav')
            self.mlp_clf2 = joblib.load(path + '\\news\\task_module\\nlp_material\\mlp_clf2.sav')
            if os.path.exists(path + '\\news\\task_module\\backup_data\\') == False:
                os.mkdir(path + '\\news\\task_module\\backup_data\\')
        self.doc_set['token'] = self.doc_set['token'].apply(lambda x: x.replace("['","").replace("']","").split("', '"))
        self.Naver = NaverNewsCrawler()
        print("datasend start!")

    def noun_corpus(self, sents):
        noun_extractor = NewsNounExtractor()
        nouns = noun_extractor.train_extract(sents)
        from soynlp.tokenizer import NounLMatchTokenizer
        noun_scores = {noun:score[0] for noun, score in nouns.items() if len(noun) > 1}
        tokenizer = NounLMatchTokenizer(noun_scores)
        corpus = [tokenizer.tokenize(sent) for sent in sents]
        return corpus

    def stopwords_remove(self, stops,corpus):
        docs=[]
        for i in range(len(corpus)):
            words=[]
            for w in corpus[i]:
                if (not w in stops) & (len(w)>1):
                    words.append(w)
            docs.append(words)
        return docs

    def make_professor_token(self, doc_df):
        worrd_list = []
        # 텍스트를 가지고 있는 리스트
        for i in list(doc_df['content']):
            # 숫자 및 특수문자 제거.
            t = re.sub('[\d\s0-9]',' ',str(i)).strip()
            t = re.sub('[=+,#/\?:^$.@*\"※~&%ㆍ·⌬◎◳▢▪!』․\\‘|\(\)\[\]\<\>`\'…》→’“”;●•]', ' ', t)
            t = re.sub(r'\xad', ' ', t)
            t = re.sub(r'\n', ' ', t)
            t = re.sub('  ', ' ', t)
            t = re.sub('  ', ' ', t)
            t = re.sub('  ', ' ', t)
            t = re.sub('및', '', t)
            worrd_list.append(t)
        df_corpus = self.noun_corpus(worrd_list)
        #stopwords 제거
        stops = list(self.ko_stopwords['stopwords'])
        docs=[]
        for i in range(len(df_corpus)):
            words=[]
            for w in df_corpus[i]:
                if (not w in stops) & (len(w)>1):
                    words.append(w)
            docs.append(words)
        return docs

    def make_professor_content(self):
        professor = self.Naver.naver_crawler_exe(mode='professor')
        text=[]
        for i in range(len(professor)):
            url = professor['link'][i]
            a = Article(url, language='ko')
            a.download()
            a.parse()
            text.append(a.text)
        professor['content'] = text
        professor['token'] = self.make_professor_token(professor)
        return professor

    def professor_news_zifslow(self):
        professor = self.make_professor_content()
        tokens = [t for d in professor['token'] for t in d]
        text = nltk.Text(tokens, name='NMSC')
        fdist = text.vocab()
        df_fdist = pd.DataFrame.from_dict(fdist, orient='index')
        df_fdist.columns = ['frequency']
        df_fdist['term'] = list(df_fdist.index)
        df_fdist = df_fdist.reset_index(drop=True)
        df_fdist = df_fdist.sort_values(["frequency"], ascending=[False])
        df_fdist = df_fdist.reset_index(drop=True)
        df_fdist.head(100)
        zif_list = pd.DataFrame(df_fdist[(df_fdist['frequency'] <= 2)]['term'])
        zif_list.columns = ['stopwords']
        zif_list = zif_list.reset_index(drop=True)
        zif_stops = list(zif_list['stopwords'])
        print(zif_stops)
        docs = self.stopwords_remove(zif_stops, professor['token'])
        docs = self.stopwords_remove(self.token_stops, docs)
        professor['token'] = docs
        professor['lable'] = ['']*len(professor)
        tagged_professor_docs = [TaggedDocument(d, c) for d, c in professor[['token', 'lable']].values]

        category_dic = {}
        big = list(set(self.doc_set['new_class']))
        for i in range(len(big)):
            temp = big[i]
            s_temp = list (set(self.doc_set[self.doc_set['new_class']==temp].new_small_class))
            category_dic[temp]=s_temp
        return category_dic, tagged_professor_docs, professor

    def professor_prediction(self):
        category_dic, tagged_professor_docs, professor = self.professor_news_zifslow()
        X_professor = [self.doc_vectorizer.infer_vector(doc.words) for doc in tagged_professor_docs]
        # y_professor = [doc.tags for doc in tagged_professor_docs]
        y_professor_pred = self.mlp_clf.predict(X_professor)
        y_professor_prob = self.mlp_clf.predict_proba(X_professor)
        L = np.argsort(-y_professor_prob, axis=1)
        two_pred = L[:,0:3]
        class_dic = {self.mlp_clf.classes_[i]: i for i in range(len(self.mlp_clf.classes_))}
        key_list = list(class_dic.keys())
        val_list = list(class_dic.values())

        dd = []
        for i in range(len(y_professor_prob)):
            first = two_pred[i][0]
            second = two_pred[i][1]
            thrid = two_pred[i][2]
            label = list([key_list[val_list.index(first)],key_list[val_list.index(second)],key_list[val_list.index(thrid)]])
            dd.append({'title':professor['title'][i],
                       'predicted_label1':label[0], 'predicted_label2': label[1], 'predicted_label3': label[2]})

        y_professor_pred = self.mlp_clf2.predict(X_professor)
        y_professor_pred = self.mlp_clf2.predict_proba(X_professor)
        L = np.argsort(-y_professor_pred, axis=1)
        two_pred = L[:,0:3]
        class_dic = {self.mlp_clf2.classes_[i]: i for i in range(len(self.mlp_clf2.classes_))}
        key_list = list(class_dic.keys())
        val_list = list(class_dic.values())

        second_result = []
        for i in range(len(X_professor)):
            tt = category_dic[dd[i]['predicted_label1']] + category_dic[dd[i]['predicted_label2']]
            tt = [x for x in tt if x in key_list]
            ttt = list({ your_key: class_dic[your_key] for your_key in tt }.values())
            tttt = [x for x in L[i] if x in ttt]
            first = tttt[0]
            second = tttt[1]
            third = tttt[2]
            label = list([key_list[val_list.index(first)],key_list[val_list.index(second)],key_list[val_list.index(third)]])
            second_result.append({'date':professor['date'][i],'title':professor['title'][i],
                                   'predicted_label1':label[0], 'predicted_label2': label[1],
                                 'link':professor['link'][i],'press':professor['press'][i]})

        professor_result = pd.DataFrame(second_result,columns=['date','title','predicted_label1','predicted_label2','link','press'])
        return professor_result
