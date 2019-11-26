from __future__ import absolute_import
# from celery import shared_task
# from celery.decorators import task
from information.task_module.rescue_crawler import RescueCrawler
from information.task_module.dart_crawler import DartUpdate
from information.models import Rescue, Dart
import os
import time
from datetime import datetime

def rescue_send(data):
    data['date'] = data['date'].apply(lambda x:str(x).replace('.','-'))
    rescue_list = []
    for i in range(data.shape[0]):
        date = data.loc[i,'date']
        area = data.loc[i,'area']
        case_num = data.loc[i,'case_num']
        company_name = data.loc[i,'company']
        court = data.loc[i,'court']
        subject = data.loc[i,'subject']
        category = data.loc[i,'company_category']
        contents = data.loc[i,'html']
        news_title = data.loc[i,'news_title']
        news_url = data.loc[i,'news_url']
        address = data.loc[i,'address2']
        ceo = data.loc[i,'ceo']
        if i % 200 == 0:
            print(date)
            print(address)
        rescue_obj = Rescue(date=date, area=area, case_num=case_num, company_name=company_name, \
                            court=court, subject=subject, category=category, contents=contents,\
                            news_title=news_title, news_url=news_url, address=address, ceo=ceo)
        rescue_list.append(rescue_obj)
    Rescue.objects.bulk_create(rescue_list)
    print('회생법인 업로드')


def dart_send(data):
    data['회사코드'] = data['회사코드'].apply(lambda x:str(x).zfill(6))
    dart_list = []
    for i in range(data.shape[0]):
        print(i)
        company_name = data.loc[i,'공시대상회사']
        ticker = data.loc[i,'회사코드']
        date = datetime.strptime(str(data.loc[i,'공시접수일자']), "%Y%m%d").date().strftime("%Y-%m-%d")
        print(date)
        contents_cat = data.loc[i,'rpt_nm']
        another_name = data.loc[i,'타법인명']
        contents = data.loc[i,'문서내용']
        news_title = str(data.loc[i,'뉴스기사제목'])
        news_url = str(data.loc[i,'뉴스기사Url'])
        if news_url == 'nan':
            news_url = None
        dart_obj = Dart(company_name=company_name, ticker=ticker,\
                        date=date, another_name=another_name, contents=contents,\
                        contents_cat=contents_cat, news_title=news_title, news_url=news_url)
        dart_list.append(dart_obj)
    Dart.objects.bulk_create(dart_list)
    print('Dart 공시자료 업로드')



# @shared_task
# @task(name="rescue-send")
def rescue_data_send():
    start_time = time.time()
    r = RescueCrawler()
    rescue_dart = r.rescue_crawling()
    rescue_dart.fillna('None', inplace=True)
    path = os.getcwd()
    rescue_dart.to_csv(path + '/information/task_module/backup/rescue/' + datetime.today().strftime("%Y%m%d")+'_rescue_court.csv',  encoding = "utf-8-sig", header=True, index=False)
    rescue_send(rescue_dart)
    end_time = time.time()
    return True, (end_time - start_time), "Data send complete"

# @task(name="dart-send")
def dart_data_send():
    start_time = time.time()
    du = DartUpdate()
    dart_result = du.make_dart_data()
    dart_result.fillna('None', inplace=True)
    path = os.getcwd()
    dart_result.to_csv(path + '/information/task_module/backup/rescue/' + datetime.today().strftime("%Y%m%d")+'_dart.csv',  encoding = "utf-8-sig", header=True, index=False)
    dart_send(dart_result)
    end_time = time.time()
    return True, (end_time - start_time),  "Data send complete"