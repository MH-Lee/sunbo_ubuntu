import time
import pandas as pd
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from news.task_module.professor import ProfessorNews
from news.task_module.news_crawler import NaverNewsCrawler
from django.db.models import Q
from .models import (LPCompany, 
                    MainCompany, 
                    InvestNews,
                    Professor,
                    Portfolio,
                    NewsUpdateCheck,
                    ProfessorUpdateCheck               
                    )
import os, platform

# Create your views here.
# main_company_view
def LP_company_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                lp_company_obj = LPCompany.objects.all().order_by(order_by)
            else:
                lp_company_obj = LPCompany.objects.all().order_by('-{}'.format(order_by))
        else:   
            try:
                lp_company_obj = LPCompany.objects.filter(
                    Q(media__icontains=query) | Q(news_title__icontains=query) |\
                    Q(company_name__icontains=query) | Q(category__icontains=query)|\
                    Q(date=query)
                ).order_by('-id')
                direction = None
            except:
                lp_company_obj = LPCompany.objects.all().order_by('-date')    
                direction = None
    else:
        lp_company_obj = LPCompany.objects.all().order_by('-date')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(lp_company_obj, 15)
        lp_company_info = paginator.get_page(page)
    except:
        paginator = Paginator(lp_company_obj, 15)
        lp_company_info = None
    return render(request, 'news/lp_company_list.html', {'lp_company_info':lp_company_info,\
                                                        'order_by':order_by, 'direction':direction})

# main_company_view
def main_company_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                main_company_obj = MainCompany.objects.all().order_by(order_by)
            else:
                main_company_obj = MainCompany.objects.all().order_by('-{}'.format(order_by))
        else:   
            try:
                main_company_obj = MainCompany.objects.filter(
                    Q(media__icontains=query) | Q(news_title__icontains=query) |\
                    Q(company_name__icontains=query) | Q(category__icontains=query) |\
                    Q(date=query)
                ).order_by('-date')
                direction = None
            except:
                main_company_obj = MainCompany.objects.all().order_by('-date') 
                direction = None   
    else:
        main_company_obj = MainCompany.objects.all().order_by('-date')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(main_company_obj, 15)
        main_company_info = paginator.get_page(page)
    except:
        paginator = Paginator(main_company_obj, 15)
        main_company_info = None
    return render(request, 'news/main_company_list.html', {'main_company_info':main_company_info,\
                                                            'order_by':order_by, 'direction':direction})

# portfolio_view
def portfolio_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                _port_obj = Portfolio.objects.all().order_by(order_by)
            else:
                _port_obj = Portfolio.objects.all().order_by('-{}'.format(order_by))
        else:   
            try:
                _port_obj = Portfolio.objects.filter(
                    Q(media__icontains=query) | Q(news_title__icontains=query) |\
                    Q(company_name__icontains=query) | Q(category__icontains=query)|\
                    Q(date=query)
                ).order_by('-date')
                direction = None
            except:
                _port_obj = Portfolio.objects.all().order_by('-date')
                direction = None
    else:
        _port_obj = Portfolio.objects.all().order_by('-date')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(_port_obj, 15)
        portfolio_info = paginator.get_page(page)
    except:
        paginator = Paginator(_port_obj, 15)
        portfolio_info = None
    return render(request, 'news/portfolio_list.html', {'portfolio_info':portfolio_info, \
                                                        'order_by':order_by, 'direction':direction})

# investment_news_view
def investment_news_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                _invest_obj = InvestNews.objects.all().order_by(order_by)
            else:
                _invest_obj = InvestNews.objects.all().order_by('-{}'.format(order_by))
        else:   
            try:
                _invest_obj = InvestNews.objects.filter(
                    Q(media__icontains=query) | Q(news_title__icontains=query) |\
                    Q(date__icontains=query) | Q(date=query) 
                ).order_by('-date')
                direction = None
            except:
                _invest_obj = InvestNews.objects.all().order_by('-date')    
                direction = None
    else:
        _invest_obj = InvestNews.objects.all().order_by('-date')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(_invest_obj, 15)
        investment_info = paginator.get_page(page)
    except:
        paginator = Paginator(_invest_obj, 15)
        investment_info = None
    return render(request, 'news/investment_news_list.html', {'investment_info':investment_info, \
                                                              'order_by':order_by, 'direction':direction})


# portfolio_view
def professor_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                _professor_obj = Professor.objects.all().order_by(order_by)
            else:
                _professor_obj = Professor.objects.all().order_by('-{}'.format(order_by))
        else:   
            try:
                _professor_obj = Professor.objects.filter(
                Q(media__icontains=query) | Q(news_title__icontains=query) |\
                Q(small_class_1__icontains=query) | Q(small_class_2__icontains=query)|\
                Q(date=query)
                ).order_by('-id')
                direction = None
            except:
                _professor_obj = Professor.objects.all().order_by('-id')
                direction = None
    else:
        _professor_obj = Professor.objects.all().order_by('-id')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(_professor_obj, 15)
        professor_info = paginator.get_page(page)
    except:
        paginator = Paginator(_professor_obj, 15)
        professor_info = None
    return render(request, 'news/professor_list.html', {'professor_info':professor_info,\
                                                        'order_by':order_by, 'direction':direction})

########################################################################################################
####### Celery 오류로 인한 수동 업데이트  ################################################################
########################################################################################################
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
    for i in range(data.shape[0]):
        media = data.loc[i,'press']
        news_title = data.loc[i,'title']
        date = data.loc[i,'date']
        small_class_1 = data.loc[i,'predicted_label1']
        small_class_2 = data.loc[i,'predicted_label2']
        news_url = data.loc[i,'link']
        prof_obj = Professor(media=media, date=date, small_class_1=small_class_1, small_class_2=small_class_2,\
                            news_title=news_title, news_url=news_url)
        prof_list.append(prof_obj)
    Professor.objects.bulk_create(prof_list)
    print('교수개발 업로드')

########################################################################################################
####### manual view                     ################################################################
########################################################################################################

def professor_data_send(request):
    start_time = time.time()
    if platform.system() == 'Linux':
        path = '/home/ubuntu/sunbo_django/news/task_module'
        backup_filename = path + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Professor_Development_naver.csv"
    else:
        print(os.getcwd())
        path = os.getcwd()
        backup_filename = path + "\\news\\task_module\\backup_data\\" + datetime.today().strftime("%Y%m%d")+ "_Professor_Development_naver.csv"

    prof = ProfessorNews()
    update_check_obj = ProfessorUpdateCheck.objects.first()
    crawling_enddate = pd.to_datetime(prof.Naver.end_date).date()
    if update_check_obj == None:
        print("data_update")
        professor_last = prof.professor_prediction()
        professor_last.sort_values('date', ascending=False, inplace=True)
        professor_last.to_csv(backup_filename,  encoding = "utf-8-sig", header=True, index=False) 
        prof_send(professor_last)
        uc_obj = ProfessorUpdateCheck(recent_date=pd.to_datetime(professor_last['date'])[0].date().strftime('%Y-%m-%d'))
        uc_obj.save()
        print("data_update complete")
    else:
        date_check = pd.to_datetime(update_check_obj.recent_date).date() + timedelta(weeks=1)
        if date_check > crawling_enddate:
            print("최신데이터")
        else:
            print("data_update")
            prof = ProfessorNews()
            professor_last = prof.professor_prediction()
            professor_last.sort_values('date', ascending=False, inplace=True)
            professor_last.to_csv(backup_filename,  encoding = "utf-8-sig", header=True, index=False) 
            prof_send(professor_last)
            ProfessorUpdateCheck.objects.all().delete()
            uc_obj = ProfessorUpdateCheck(recent_date=pd.to_datetime(professor_last['date'])[0].date().strftime('%Y-%m-%d'))
            uc_obj.save()
            print("data_update complete")
    end_time = time.time()
    print(end_time - start_time)
    return redirect("/news/professor/")


def news_datasend(request):
    start_time = time.time()
    if platform.system() == 'Linux':
        path = '/home/ubuntu/sunbo_django/news/task_module'
        inv_backup_filename = path + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_Investment_attraction_naver.csv"
        com_backup_filename = path + "/backup_data/" + datetime.today().strftime("%Y%m%d")+ "_company_naver.csv"
    else:
        print(os.getcwd())
        path = os.getcwd()
        inv_backup_filename = path + "\\news\\task_module\\backup_data\\" + datetime.today().strftime("%Y%m%d")+ "_Investment_attraction_naver.csv"
        com_backup_filename = path + "\\news\\task_module\\backup_data\\" + datetime.today().strftime("%Y%m%d")+ "_company_naver.csv"

    Naver = NaverNewsCrawler()
    update_check_obj = NewsUpdateCheck.objects.first()
    crawling_enddate = pd.to_datetime(Naver.end_date).date()
    if update_check_obj == None:
        print("data_update")
        invest = Naver.naver_crawler_exe(mode='invest')
        company = Naver.naver_crawler_exe(mode='company')
        invest.sort_values('date', ascending=False, inplace=True)
        company.sort_values('date', ascending=False, inplace=True)
        invest.to_csv(inv_backup_filename,  encoding = "utf-8-sig", header=True, index=False)
        company.to_csv(com_backup_filename,  encoding = "utf-8-sig", header=True, index=False)
        invest_news_send(invest)
        company_send(company)
        uc_obj = NewsUpdateCheck(recent_date=pd.to_datetime(company['date'])[0].date().strftime('%Y-%m-%d'))
        uc_obj.save()
        print("data_update complete")
    else:
        date_check = pd.to_datetime(update_check_obj.recent_date).date() + timedelta(weeks=1)
        if date_check > crawling_enddate:
            print("최신데이터")
        else:
            print("data_update")
            invest = Naver.naver_crawler_exe(mode='invest')
            company = Naver.naver_crawler_exe(mode='company')
            invest.sort_values('date', ascending=False, inplace=True)
            company.sort_values('date', ascending=False, inplace=True)
            invest.to_csv(inv_backup_filename,  encoding = "utf-8-sig", header=True, index=False)
            company.to_csv(com_backup_filename,  encoding = "utf-8-sig", header=True, index=False)
            invest_news_send(invest)
            company_send(company)
            uc_obj = NewsUpdateCheck(recent_date=pd.to_datetime(company['date'])[0].date().strftime('%Y-%m-%d'))
            uc_obj.save()
            print("data_update complete")
    end_time = time.time()
    print(end_time - start_time)
    return redirect("/")
