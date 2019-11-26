from __future__ import absolute_import
# from celery import shared_task
from news.task_module.professor import ProfessorNews
from news.task_module.news_crawler import NaverNewsCrawler
from news.models import (InvestNews,
                        LPCompany,
                        MainCompany,
                        Portfolio,
                        Professor
                        )
from datetime import datetime
import time

def invest_news_send(data):
    invest_list = []
    for i in range(data.shape[0]):
        media = data.loc[i, 'press']
        date =  data.loc[i, 'date']
        news_title = data.loc[i, 'title']
        news_url = data.loc[i, 'link']
        invest_obj = InvestNews(media=media, date=date, news_title=news_title,\
                                news_url=news_url)
        invest_list.append(invest_obj)
    InvestNews.objects.bulk_create(invest_list)
    print('invest_news 업로드')

def company_send(data):
    main_list = []
    port_list = []
    lpc_list = []
    for i in range(data.shape[0]):
        category = data.loc[i, 'category']
        company_name  = data.loc[i, 'company']
        news_title = data.loc[i,'title']
        media = data.loc[i,'press']
        date =  data.loc[i,'date']
        news_url = data.loc[i,'link']
        if category == '포트폴리오':
            port_obj = Portfolio(category=category, company_name=company_name, media=media, date=date,\
                                news_title=news_title, news_url=news_url)
            port_list.append(port_obj)
        elif category == 'LP기업':
            lpc_obj = LPCompany(category=category, company_name=company_name, media=media, date=date,\
                                news_title=news_title, news_url=news_url)
            lpc_list.append(lpc_obj)
        elif category == '자매기업':
            main_obj = MainCompany(category=category, company_name=company_name, media=media, date=date,\
                                    news_title=news_title, news_url=news_url)
            main_list.append(main_obj)
    Portfolio.objects.bulk_create(port_list)
    print('포트폴리오 업로드')
    LPCompany.objects.bulk_create(lpc_list)
    print('LP기업 업로드')
    MainCompany.objects.bulk_create(main_list)
    print('Main기업 업로드')

def prof_send(data):
    prof_list = []
    start_time = time.time()
    for i in range(data.shape[0]):
        media = data.iloc[i,'press']
        news_title = data.loc[i,'title']
        date = data.loc[i,'date']
        small_class_1 = data.loc[i,'predicted_label1']
        small_class_2 = data.loc[i,'predicted_label2']
        news_url = data.loc[i,'link']
        prof_obj = Professor(media=media, date=date, small_class_1=small_class_1, small_class_2=small_class_2,\
                            news_title=news_title, news_url=news_url)
        prof_list.append(prof_obj)
    Professor.objects.bulk_create(prof_list)
    end_time = time.time()
    print('교수개발 업로드')
    return (end_time - start_time),  "Data request complete"

# @shared_task
def professor_data_send():
    path = '/home/ubuntu/sunbo_django/news/task_module'
    start_time = time.time()
    prof = ProfessorNews()
    professor_last = prof.professor_prediction()
    professor_last.to_csv(path + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Professor_Development_naver.csv",  encoding = "utf-8-sig", header=True, index=False) 
    end_time = time.time()
    return (end_time - start_time),  "Data request complete"

# @shared_task
def news_datasend():
    path = '/home/ubuntu/sunbo_django/news/task_module'
    start_time = time.time()
    Naver = NaverNewsCrawler()
    invest = Naver.naver_crawler_exe(mode='invest')
    company = Naver.naver_crawler_exe(mode='company')
    invest.to_csv(path + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Investment_attraction_naver.csv",  encoding = "utf-8-sig", header=True, index=False)
    company.to_csv(path + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_company_naver.csv",  encoding = "utf-8-sig", header=True, index=False)
    invest_news_send(invest)
    company_send(company)
    end_time = time.time()
    return (end_time - start_time),  "Data request complete"