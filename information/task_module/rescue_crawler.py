import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import ast
import os
import sys
from urllib.request import urlopen
from datetime import datetime, timedelta, date
from traceback import format_exc
import json
import math
import urllib.error
from urllib.parse import quote
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import pandas as pd
import platform

js = """
<script language="javascript" type="text/javascript">
&lt;!--
function MM_reloadPage(init) {  //reloads the window if Nav4 resized
  if (init==true) with (navigator) {if ((appName=="Netscape")&amp;&amp;(parseInt(appVersion)==4)) {
    document.MM_pgW=innerWidth; document.MM_pgH=innerHeight; onresize=MM_reloadPage; }}
  else if (innerWidth!=document.MM_pgW || innerHeight!=document.MM_pgH) location.reload();
}
MM_reloadPage(true);
//--&gt;
</script>
<link href="/wbi.css" rel="stylesheet" type="text/css"/>
"""
caption = """
<caption="특별조사기일 style="display:inline !important; visibility:visible !important; width:1px; height:1px; font-size:0px; overflow:hidden; line-height:0; " 공고"="" 관계인집회기일="" 및="" 제2,3회="">
</caption="특별조사기일><table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%">
"""
str1 = """<td height="33" style="padding-left:20px"><img alt="로고" src="/img/hpgonggo/logo_scourt.gif"/></td>"""
str2 = """<td height="27"><img alt="종료" border="0" onclick="window.close();" src="/img/hpgonggo/btn_close.gif" style="cursor:hand"/><img alt="공백" height="10" src="/img/hpgonggo/blank.gif" width="10"/></td>"""

class RescueCrawler:
    def __init__(self, term=1):
        self.start_date = datetime.today() - timedelta(1)
        self.start_date = self.start_date.strftime("%Y.%m.%d")
        term = -1 * term
        self.end_date = date.today() + timedelta(weeks=term)
        self.end_date = self.end_date.strftime("%Y.%m.%d")
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.rescue_url = 'http://safind.scourt.go.kr/sf/hpbigonggo/whp_gonggo.jsp?org_bub_nm=&amp;theme=#'
        self.naver_news = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
        self.naver_news_content = 'https://search.naver.com/search.naver?&where=news&query={}&start=1&sort=sim&field=0&pd=6'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        if os.path.exists(self.path + '/task_module/backup/') == False:
            print('backup 생성')
            os.mkdir(self.path + '/task_module/backup')
        if os.path.exists(self.path + '/task_module/backup/rescue/') == False:
            os.mkdir(self.path + '/task_module/backup/rescue')
        print("collect rescue case {} weeks ago".format(term), self.path)

    def get_content (self, driver,area,start_date,end_date) :
        final_result = pd.DataFrame()
        #for area in area_list :
        print(area)
        driver.get(self.rescue_url)
        driver.implicitly_wait(5)

        select = Select(driver.find_element_by_xpath("//select[@id='sel_map']"))
        select.select_by_visible_text('법인회생')
        driver.implicitly_wait(3)

        select = Select(driver.find_element_by_xpath("//select[@id='area']"))
        select.select_by_visible_text(area)
        driver.implicitly_wait(3)

        driver.find_element_by_xpath('//*[@id="contants"]/div[2]/div[18]/a').click()
        driver.implicitly_wait(5)

        temp = self.get_info(driver,area,start_date,end_date)
        print(len(temp))
        final_result = final_result.append(temp, ignore_index=True)
        return final_result

    def get_info(self, driver,area,start_date,end_date):
        area = area
        last_date = start_date
        info = []
        i,j = 0,0
        while last_date > end_date:
            i = i+1
            driver.implicitly_wait(3)
            try:
                driver.find_element_by_xpath('/html/body/div/div[4]/a['+str(i)+']').click()
                j = j+1
                if j == 11 :
                    i,j = 2,1
            except NoSuchElementException:
                last_date = end_date
            else:
                driver.implicitly_wait(3)
                html = driver.page_source ## 페이지의 elements모두 가져오기
                soup = BeautifulSoup(html, 'html.parser') ## BeautifulSoup사용하기
                contents = soup.select('body > div > table > tbody > tr ')
                k = 1
                for content in contents:
                    date = content.find_all("td")[3].text
                    if date > start_date:
                        k = k+1
                    else:
                        case_num = content.find_all("td")[0].text
                        court = content.find_all("td")[1].text
                        company = content.find_all("td")[2].text
                        subject = content.find_all("td")[4].text
                        subject = re.sub('[\n\t]', '', subject).strip()
                        driver.find_element_by_xpath('/html/body/div/table/tbody/tr['+str(k)+']/td[6]/a').click()
                        driver.switch_to_window(driver.window_handles[1])
                        time.sleep(1)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        sub_info = soup.select('font > p')
                        if len(sub_info) == 2 :
                            address = sub_info[0].text
                            # ceo = sub_info[1].text
                        elif len(sub_info) == 1:
                            address = sub_info[0].text
                            # ceo = 'none'
                        else :
                            address = 'none'
                            # ceo = 'none'

                        if(date < end_date):
                            last_date = date
                            break
                        else :
                            info.append({'area':area,'case_num' : case_num,'court' : court,'company' :company,\
                                         'date':date ,'subject' :subject,'sub_info':sub_info,'html':soup, 'address':address})
                            driver.switch_to_window(driver.window_handles[0])
                            k = k+1
        dataframe = pd.DataFrame(info)
        #driver.close()
        return dataframe


    def get_news_content_keyword(self, final_result):
        naver_news_address = []
        for i in range(0,len(final_result)):
            comapny = final_result['company'][i]
            company_name = comapny.replace("주식회사","").replace("(주)","").replace("분할존속회사","").replace("분할신설회사","").strip()
            search_keyword = company_name + ' 회생 ' + '"'+company_name+'"' + ' "회생"'
            encode_search_keyword = urllib.parse.quote(search_keyword) ## 입력한 키워드를 url에 넣을 수 있도록 parsing 변환
            url = self.naver_news_content.format(encode_search_keyword)
            req = requests.get(url) ## HTTP GET Request
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            my_titles_sub = soup.select('dl > dt > a')

            for title in my_titles_sub:
                if title.get('href') != '#':
                    # html = '<a href = "{}" target="_blank" > {} </a> '.format(title.get('href'),title.get('title'))
                    news_title = title.get('title')
                    news_url = title.get('href')
                    naver_news_address.append({'company': final_result['company'][i],
                                               'news_title': news_title, 'news_url':news_url}) #url 가져오기
                if len(naver_news_address) > 0 :
                    break
        return naver_news_address

    def get_company_keyword(self, rescue):
        name=[]
        category=[]
        detailed_info=[]
        for i in range(len(rescue)):
            encode_search_keyword = urllib.parse.quote(rescue['company'][i]) ## 입력한 키워드를 url에 넣을 수 있도록 parsing 변환
            url = self.naver_news + encode_search_keyword
            req = requests.get(url) ## HTTP GET Request
            html = req.content
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if soup.find('div',class_ = 'sp_company sc _au_company_search _au_company_answer'):
                    item_list=[]
                    info=[]
                    temp1=soup.find('div',class_ = 'sp_company sc _au_company_search _au_company_answer')
                    category.append(temp1.find('div', class_ = 'company_intro _ellipsis _detail').text.strip())
                    temp3=temp1.find_all('span', class_ = 'tit ',text=True)
                    temp4=temp1.find_all('span', class_ = 'txt_info ')
                    for j in range(len(temp3)-1):
                        item_list.append(temp3[j].text.strip())
                    for j in range(len(temp3)-1):
                        info.append(temp4[j].text.strip())
                    detailed_info.append(dict(zip(item_list, info)))
                else:
                    temp2=soup.find('div',class_ = 'sp_company sc _au_company_search _company_same_name')
                    d1=[]
                    d2=[]
                    if temp2.find('span', class_ = 'sub_tit'):
                        for k in range(len(temp2.find_all('span', class_ = 'sub_tit'))):
                            d1.append(temp2.find_all('span', class_ = 'sub_tit')[k].text.strip())
                            d2.append(temp2.find_all('div', class_ = 'item_txt')[k].text.strip())
                        df=pd.DataFrame({'기업분류':d1,'세부정보':d2})
                        df_new=df.loc[pd.Series(df['세부정보']).str.contains(rescue['ceo'][i])]['기업분류']
                        df_new=df_new.reset_index(drop=True)
                        category.append(df_new[0])
                        detailed_info.append('None')
                    else:
                        for kk in range(len(temp2.find_all('span', class_ = 'info_sub'))):
                            d1.append(temp2.find_all('span', class_ = 'info_sub')[kk].text.strip())
                            d2.append(temp2.find_all('span', class_ = 'info_txt')[kk].text.strip())
                        df=pd.DataFrame({'기업분류':d1,'세부정보':d2})
                        df_new=df.loc[pd.Series(df['세부정보']).str.contains(rescue['ceo'][i])]['기업분류']
                        df_new=df_new.reset_index(drop=True)
                        category.append(df_new[0])
                        detailed_info.append('None')
            except AttributeError:
                #print(e)
                category.append('None')
                detailed_info.append('None')
            except IndexError:
                #print(i,e)
                category.append('None')
                detailed_info.append('None')
            name.append(rescue['company'][i])

        final_data = pd.DataFrame({'기업명':name,'기업분류':category, '세부정보':detailed_info})
        rescue['company_category']=final_data['기업분류']
        rescue['detailed_info']=final_data['세부정보']
        return rescue

    def catch_address(self, address):
        if address != 'none':
            result = address.split('       ')[2].replace("\n", "")
        else:
            result = 'none'
        return result

    def html_refine(self, html):
        result = str(html).replace(str1, "").replace(str2, "").replace(js, "").replace(caption,"")
        return result

    def rescue_crawling(self):
        area_list = ['서울','의정부','인천','수원','춘천','대전','청주','대구','부산','울산','창원','광주','전주','제주']
        final_result = pd.DataFrame()
        for area in area_list:
            if platform.system() == 'Linux':
                driver = webdriver.Chrome(r'/usr/lib/chromium-browser/chromedriver', options=self.options)
            else:
                driver = webdriver.Chrome('.\\information\\task_module\\chromedriver', options=self.options)
            driver.implicitly_wait(5)
            temp = self.get_content(driver, area, self.start_date, self.end_date)
            #driver.close()
            driver.quit()
            final_result = final_result.append(pd.DataFrame(data = temp), ignore_index=True)

        ceo = []
        for i in range(len(final_result)):
            if len(final_result['sub_info'][i]) == 2 :
                ceo.append(re.sub('[\n\xa0]', '', final_result['sub_info'][i][1].text).strip())
            elif len(final_result['sub_info'][i]) == 1 :
                ceo.append('none')
            else:
                ceo.append('none')

        final_result['address2'] = final_result['address'].apply(lambda x: self.catch_address(x))
        final_result['html'] = final_result['html'].apply(lambda x:self.html_refine(x))
        # final_result['html'] = final_result['html'].apply(str)
        final_result['ceo'] = ceo
        del final_result['sub_info']
        news_result = self.get_news_content_keyword(final_result)
        rescue = pd.merge(pd.DataFrame(news_result),final_result,on='company',how='right').drop_duplicates().reset_index(drop=True)
        final_result = self.get_company_keyword(rescue)
        final_result = final_result.drop_duplicates(subset='case_num', keep="first").reset_index(drop=True)
        return final_result


# from information.task_module.rescue_crawler import RescueCrawler
# r = RescueCrawler()
# final_result = r.rescue_crawling()
# final_result.fillna('None', inplace=True)
# import os
# path = os.getcwd()
# from datetime import datetime
# final_result.to_csv(path + '/information/task_module/backup/rescue/' + datetime.today().strftime("%Y%m%d")+'_rescue_court.csv',  encoding = "utf-8-sig", header=True, index=False)
