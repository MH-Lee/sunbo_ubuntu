import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from datetime import datetime, timedelta, date
import math
import urllib.error
import urllib.parse
import time
import pandas as pd
import numpy as np
import platform
import os


class NaverNewsCrawler:
    def __init__(self):
        if platform.system() == 'Linux':
            path = '/home/ubuntu/sunbo_django/news/task_module'
            self.company_list = pd.read_excel(path + '/nlp_data/company_list.xlsx')
            self.stopwords = pd.read_excel(path + '/nlp_data/crawling_stopwords.xlsx')
        else:
            print(os.getcwd())
            path = os.getcwd()
            self.company_list = pd.read_excel(path + '\\news\\task_module\\nlp_data\\company_list.xlsx')
            self.stopwords = pd.read_excel(path + '\\news\\task_module\\nlp_data\\crawling_stopwords.xlsx')
        self.naver_total_page = 'https://search.naver.com/search.naver?&where=news&query={}&start=1&sort=1{}'
        self.naver_search_url = 'https://search.naver.com/search.naver?&where=news&query={}&start={}&sort=1{}'
        self.end_date = date.today() - timedelta(1)
        self.end_date = self.end_date.strftime("%Y.%m.%d")
        self.start_date = date.today() + timedelta(weeks=-1)
        self.start_date = self.start_date.strftime("%Y.%m.%d")
        self.naver_date = '&pd=3&ds=' + self.start_date+'&de=' + self.end_date


        print("news crawler start!")

    def get_total_page(self, search_keyword,period,search_type):
        encode_search_keyword = urllib.parse.quote(search_keyword) ## 입력한 키워드를 url에 넣을 수 있도록 parsing 변환
        # url = 'https://search.naver.com/search.naver?&where=news&query='+encode_search_keyword+ '&start=1&sort=1'+search_type+period
        url = self.naver_total_page.format(encode_search_keyword, search_type+period)
        req = requests.get(url) ## HTTP GET Request
        status = req.status_code ## HTTP Status 가져오기 (200: 정상)
        if status == 200 :
            html = req.text ## HTML 소스 가져오기
            soup = BeautifulSoup(html, 'html.parser') ## BeautifulSoup으로 html소스를 python객체로 변환하기
            page_info = soup.find_all('div',class_ = 'title_desc all_my') ## total page 정보 가져오기
            page_index1 = str(page_info).find('/')
            page_index2 = str(page_info).find('건')
            if page_index1 != -1 : ## total_index = -1 이면 0 건
                total_num = int(str(page_info)[page_index1+1:page_index2].replace(",",""))
                total_page = math.ceil(total_num / 10)
            else : total_page = 0
        else:
            total_page = 0
        return total_page

    def get_news_url(self, search_keyword, period, search_type):
        encode_search_keyword = urllib.parse.quote(search_keyword) ## 입력한 키워드를 url에 넣을 수 있도록 parsing 변환
        total_page = self.get_total_page(search_keyword,period,search_type) ## get_total_gage
        naver_news_address = [] # url 저장 될 list 생성
        for i in range(total_page):
            #if i > 40 : break
            # url = 'https://search.naver.com/search.naver?&where=news&query='+encode_search_keyword+ '&start='+str(i*10 +1)+'&sort=1'+search_type+period
            url = self.naver_search_url.format(encode_search_keyword, str(i*10 +1), search_type+period)
            req = requests.get(url) ## HTTP GET Request
            status = req.status_code ## HTTP Status 가져오기 (200: 정상)
            if status == 200:
                html = req.text ## HTML 소스 가져오기
                soup = BeautifulSoup(html, 'html.parser') ## BeautifulSoup으로 html소스를 python객체로 변환하기
                my_titles_sub = soup.select('dl > dt > a')
                #my_titles_sub = soup.select('dd > a')
                for title in my_titles_sub:
                    if title.get('href') != '#':
                        naver_news_address.append(title.get('href')) #url 가져오기
        return naver_news_address

    def get_news_total(self, keyword,period,search_type):
        search_keyword = keyword
        encode_search_keyword = urllib.parse.quote(search_keyword) ## 입력한 키워드를 url에 넣을 수 있도록 parsing 변환
        total_page = self.get_total_page(search_keyword,period,search_type) ## get_total_gage
        print('total page: ' + str(total_page))
        title_list = []
        link_list  = []
        press_list = []
        date_list  = []
        for j in range(total_page):
            url = 'https://search.naver.com/search.naver?&where=news&query='+encode_search_keyword+ '&start='+str(j*10 +1)+'&sort=1'+search_type+period
            req = requests.get(url)
            status = req.status_code
            if status == 200:
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')
                my_titles_sub = soup.select('li > dl > dt > a')
                my_date_sub = soup.select('dl > dd.txt_inline')
                for k in range(len(my_titles_sub)):
                    if '일 전' in str(my_date_sub[k]).split('<span class="bar"></span>')[1] :
                        day = str(my_date_sub[0]).split('<span class="bar"></span>')[1]
                        day = int(re.findall("\d",day)[0])
                        date_t = date.today() - timedelta(day)
                        date_t = date_t.strftime("%Y/%m/%d")
                    else :
                        date_t = date.today() - timedelta(1)
                        date_t = date_t.strftime("%Y/%m/%d")
                    title = my_titles_sub[k].get('title')
                    link  = my_titles_sub[k].get('href')
                    info  = my_date_sub[k].text.split(' ')
                    press = info[0]
                    title_list.append(title)
                    link_list.append(link)
                    press_list.append(press)
                    date_list.append(date_t)
        dataframe = pd.DataFrame({'title':title_list,'link':link_list,'press':press_list,'date':date_list})
        return dataframe

    def get_news_company(self, period, search_type):
        dataframe = pd.DataFrame(columns=['company','category','title','press','link','date'])
        company_list = self.company_list
        for i in range(len(company_list)):
            company = company_list['기업명'][i]
            category = company_list['구분'][i]
            search_keyword = company_list['기업명'][i]+' "'+company_list['Input'][i]+'"'
            temp = self.get_news_total(search_keyword,period,search_type)
            temp['company'] = [company_list['기업명'][i]]*len(temp)
            temp['category'] = [company_list['구분'][i]]*len(temp)
            dataframe = dataframe.append(pd.DataFrame(data = temp), ignore_index=True)
        return dataframe

    def remove_dupli(self, dataframe):
        title = dataframe['title']
        for i in range(len(title)):
            title[i] = re.sub('[\'\",.\(\)\[\]\·]',' ',title[i])

        du_list = []
        for i in range(len(title)):
            if i not in du_list:
                a = title[i].split(' ')
                for j in range(len(title)):
                    if i != j:
                        b = title[j].split(' ')
                        du = len(set(a) & set(b))
                        pro = (du*2)/(len(a)+len(b))
                        if pro > 0.4 :
                            du_list.append(j)
        temp = dataframe.index.isin(du_list)
        return dataframe[~temp].reset_index(drop=True)

    def naver_crawler_exe(self, mode='professor'):
        if mode == 'professor':
            keyword_result1 = self.get_news_total('교수 개발', self.naver_date, '&field=1')
            # result_df = self.remove_dupli(keyword_result1)
            Professor_Development = self.remove_dupli(keyword_result1)
            # print(Professor_Development)
            Professor_Development['date'] = Professor_Development['date'].apply(lambda x: x.replace('/', '-'))
            
            result_df = Professor_Development[~Professor_Development.title.str.contains('|'.join(list(self.stopwords[self.stopwords['type']=='PD']['stopwords'])))].reset_index(drop=True)
        elif mode == 'invest':
            keyword_result2 = self.get_news_total('투자 유치', self.naver_date, '&field=1')
            Investment_attraction = self.remove_dupli(keyword_result2)
            Investment_attraction['date'] = Investment_attraction['date'].apply(lambda x: x.replace('/', '-'))
            result_df = Investment_attraction[~Investment_attraction.title.str.contains('|'.join(list(self.stopwords[self.stopwords['type']=='IA']['stopwords'])))].reset_index(drop=True)
        else:
            company_news = self.get_news_company(self.naver_date, '&field=0')
            company_news2 = self.remove_dupli(company_news)
            company_news2['date'] = company_news2['date'].apply(lambda x: x.replace('/', '-'))
            result_df = company_news2[~company_news2.title.str.contains('|'.join(list(self.stopwords[self.stopwords['type']=='CN']['stopwords'])))].reset_index(drop=True)
        return result_df
