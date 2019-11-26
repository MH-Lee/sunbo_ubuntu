from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Rescue, Dart, DartUpdateCheck, RescueUpdateCheck
import pandas as pd

# Create your views here.
def rescue_detail(request, pk):
    try:
        rescue = Rescue.objects.get(pk=pk)
    except Rescue.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render(request, 'information/rescue_detail.html', {'rescue':rescue})

def rescue_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                rescue_obj = Rescue.objects.all().order_by(order_by)
            else:
                rescue_obj = Rescue.objects.all().order_by('-{}'.format(order_by))
        else:   
            try:
                rescue_obj = Rescue.objects.filter(
                    Q(area__icontains=query) | Q(case_num__icontains=query) |\
                    Q(subject__icontains=query) | Q(company_name__icontains=query) |\
                    Q(category__icontains=query) | Q(news_title__icontains=query) |\
                    Q(date=query)
                ).order_by('-date')
                direction = None
            except:
                rescue_obj = Rescue.objects.all().order_by('-date')
                direction = None
    else:
        rescue_obj = Rescue.objects.all().order_by('-date')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(rescue_obj, 15)
        rescues = paginator.get_page(page)
    except:
        paginator = Paginator(rescue_obj, 15)
        rescues = None
    index = rescues.number -1 
    max_index = len(paginator.page_range) 
    start_index = index -2 if index >= 2 else 0 
    if index < 2 : 
        end_index = 5-start_index 
    else : 
        end_index = index+3 if index <= max_index - 3 else max_index 
    page_range = list(paginator.page_range[start_index:end_index]) 
    return render(request, 'information/rescue_list.html', {'rescues':rescues, 'order_by':order_by , 'direction':direction,\
                                                            'page_range':page_range, 'max_index':max_index-2})

# dart_view
def dart_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                darts = Dart.objects.all().order_by(order_by)
            else:
                darts = Dart.objects.all().order_by('-{}'.format(order_by))
        else:   
            try:
                darts = Dart.objects.filter(
                    Q(company_name__icontains=query) | Q(news_title__icontains=query) |\
                    Q(another_name__icontains=query) | Q(date=query)
                ).order_by('-date')
                direction = None
            except:
                darts = Dart.objects.all().order_by('-date')
                direction = None
    else:
        darts = Dart.objects.all().order_by('-date')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(darts, 15)
        dart_infos = paginator.get_page(page)
    except:
        paginator = Paginator(darts, 15)
        dart_infos = None
    return render(request, 'information/dart_list.html', {'dart_infos':dart_infos, 'order_by':order_by, 'direction':direction})

########################################################################################################
####### Celery 오류로 인한 수동 업데이트  ################################################################
########################################################################################################
from information.task_module.rescue_crawler import RescueCrawler
from information.task_module.dart_crawler import DartUpdate
from datetime import datetime, timedelta, date
import os
import time
import platform

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
                            news_title=news_title, news_url=news_url, company_address=address, ceo=ceo)
        rescue_list.append(rescue_obj)
    Rescue.objects.bulk_create(rescue_list)
    print('회생법인 업로드')

def dart_send(data):
    data['회사코드'] = data['회사코드'].apply(lambda x:str(x).zfill(6))
    data['공시접수일자'] = data['공시접수일자'].apply(lambda x:  datetime.strptime(str(x), "%Y%m%d").strftime("%Y-%m-%d"))
    dart_list = []
    for i in range(data.shape[0]):
        print(i)
        company_name = data.loc[i,'공시대상회사']
        ticker = data.loc[i,'회사코드']
        date = data.loc[i,'공시접수일자']
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

def rescue_data_send(request):
    start_time = time.time()
    print(os.getcwd())
    path = os.getcwd()
    if platform.system() == 'Linux':
        # path = '/home/ubuntu/sunbo_django/information/task_module'
        backup_filename = path + "/information/task_module/backup/rescue/" + datetime.today().strftime("%Y%m%d")+ "_rescue_court.csv"
    else:
        backup_filename = path + "\\information\\task_module\\backup\\rescue\\" + datetime.today().strftime("%Y%m%d")+ "_rescue_court.csv"

    r = RescueCrawler(term=2)
    update_check_obj = RescueUpdateCheck.objects.first()
    crawling_enddate = pd.to_datetime(r.end_date).date()
    if update_check_obj == None:
        print("data_update")
        rescue_data = r.rescue_crawling()
        rescue_data.fillna('None', inplace=True)
        rescue_data.sort_values('date', ascending=False, inplace=True)
        rescue_data.to_csv(backup_filename,  encoding = "utf-8-sig", header=True, index=False)
        rescue_send(rescue_data)
        RescueUpdateCheck.objects.all().delete()
        uc_obj = RescueUpdateCheck(recent_date=pd.to_datetime(rescue_data['date'])[0].date().strftime('%Y-%m-%d'))
        uc_obj.save()
        print("data_update complete")
    else:
        date_check = pd.to_datetime(update_check_obj.recent_date).date() + timedelta(weeks=1)
        if date_check > crawling_enddate:
            print("최신데이터")
        else:
            print("data_update")
            rescue_data = r.rescue_crawling()
            rescue_data.fillna('None', inplace=True)
            rescue_data.sort_values('date', ascending=False, inplace=True)
            rescue_data.to_csv(backup_filename,  encoding = "utf-8-sig", header=True, index=False)
            rescue_send(rescue_data)
            RescueUpdateCheck.objects.all().delete()
            uc_obj = RescueUpdateCheck(recent_date=pd.to_datetime(rescue_data['date'])[0].date().strftime('%Y-%m-%d'))
            uc_obj.save()
            print("data_update complete")
    end_time = time.time()
    print(end_time - start_time)
    return redirect("/information/rescue_list/")

def dart_data_send(request):
    start_time = time.time()
    print(os.getcwd())
    path = os.getcwd()
    if platform.system() == 'Linux':
        # path = '/home/ubuntu/sunbo_django/information/task_module'
        backup_filename = path + "/information/task_module/backup/dart/" + datetime.today().strftime("%Y%m%d")+ "_dart.csv"
    else:
        backup_filename = path + "\\information\\task_module\\backup\\dart\\" + datetime.today().strftime("%Y%m%d")+ "_dart.csv"

    du = DartUpdate()
    update_check_obj = DartUpdateCheck.objects.first()
    # crawling_enddate = pd.to_datetime(du.before_week).date()
    if update_check_obj == None:
        print("data_update")
        dart_result = du.make_dart_data()
        dart_result.fillna('None', inplace=True)
        dart_result.sort_values('공시접수일자', ascending=False, inplace=True)
        dart_result.to_csv(backup_filename,  encoding = "utf-8-sig", header=True, index=False)
        dart_send(dart_result)
        DartUpdateCheck.objects.all().delete()
        uc_obj = DartUpdateCheck(recent_date=pd.to_datetime(dart_result['공시접수일자'])[0].date().strftime('%Y-%m-%d'))
        uc_obj.save()
        print("data_update complete")
    else:
        date_check = pd.to_datetime(update_check_obj.recent_date).date() + timedelta(weeks=1)
        if date_check > date.today():
            print("최신데이터")
        else:
            print("data_update")
            dart_result = du.make_dart_data()
            dart_result.fillna('None', inplace=True)
            dart_result.sort_values('공시접수일자', ascending=False, inplace=True)
            path = os.getcwd()
            dart_result.to_csv(backup_filename,  encoding = "utf-8-sig", header=True, index=False)
            dart_send(dart_result)
            DartUpdateCheck.objects.all().delete()
            uc_obj = DartUpdateCheck(recent_date=pd.to_datetime(dart_result['공시접수일자'])[0].date().strftime('%Y-%m-%d'))
            uc_obj.save()
            print("data_update complete")
    end_time = time.time()
    print(end_time - start_time)
    return redirect("/information/dart_list/")