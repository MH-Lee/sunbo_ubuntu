import requests
from bs4 import BeautifulSoup
import re
import ast
import os
import sys
from urllib.request import urlopen
import json
import math
import urllib.error
from urllib.parse import quote
import pandas as pd
import lxml.html
from datetime import datetime, timedelta
from traceback import format_exc
import time


class DartUpdate:
    def __init__(self):
        self.auth_key="4f6c2a78b4550eb0169daa87515afd12e3ea2922" #인증키 입력(새로 인증키를 받는 것 추천)
        self.first_page = "http://dart.fss.or.kr/api/search.xml?auth="+ self.auth_key + "&start_dt={}&dsp_tp=B&bsn_tp=B001&page_no=1&page_set=100"
        self.dart_list_url = "http://dart.fss.or.kr/api/search.xml?auth="+ self.auth_key +"&start_dt={}&dsp_tp=B&bsn_tp=B001&page_no={}&page_set=100"
        self.naver_url = 'https://search.naver.com/search.naver?&where=news&query={}&start=1&sort=sim&field=0&pd=6'
        self.before_week = datetime.today() + timedelta(weeks=-1)

    def all_company_info(self, start_date):
        data = pd.DataFrame() #빈 데이터프레임 생성
        #1페이지의 result정보를 통해 총 page 수 확인
        result_URL=urlopen(self.first_page.format(start_date))
        result=result_URL.read()
        soup=BeautifulSoup(result,'html.parser')
        page_num=int(re.findall('\d+', soup.findAll("total_page")[0].find_all(text=True)[0])[0])
        #page 수만큼 반복
        for i in range(1,page_num+1):
            resultXML=urlopen(self.dart_list_url.format(start_date, i))
            result=resultXML.read()
            xmlsoup=BeautifulSoup(result,'html.parser')
            te=xmlsoup.findAll("list")
            for t in te:
                temp=pd.DataFrame(([[t.crp_cls.string,t.crp_nm.string,t.crp_cd.string,t.rpt_nm.string,
                    t.rcp_no.string,t.flr_nm.string,t.rcp_dt.string]]),
                    columns=["법인구분","공시대상회사","회사코드","rpt_nm","rcp_no","flr_nm","공시접수일자"])
                data=pd.concat([data,temp])
        searchfor = ['타법인주식및출자증권양수결정','타법인주식및출자증권취득결정']
        drop_for = ['첨부정정', '첨부추가']
        data=data.reset_index(drop=True)
        data = data.drop(data[pd.Series(data['rpt_nm']).str.contains('|'.join(drop_for))].index) #첨부정정 문서는 내용 X
        index_df=data[pd.Series(data['rpt_nm']).str.contains('|'.join(searchfor))].index #타법인주식및출자증권양수결정과 관련된 목록만 가져옴
        final_data=data.loc[index_df]
        final_data=final_data.reset_index(drop=True)
        return final_data

    def get_news_content_keyword(self, final_result):
        naver_news_address = []
        for i in range(0,len(final_result)):
            search_keyword = final_result['공시대상회사'][i]+' '+final_result['타법인명'][i]
            print(search_keyword)
            encode_search_keyword = urllib.parse.quote(search_keyword) ## 입력한 키워드를 url에 넣을 수 있도록 parsing 변환
            url = self.naver_url.format(encode_search_keyword)
            req = requests.get(url) ## HTTP GET Request

            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            my_titles_sub = soup.select('dl > dt > a')

            if len(my_titles_sub)>0:
                for title in my_titles_sub:
                    if title.get('href') != '#':
                        # html = '<a href = {}> {} </a> '.format(title.get('href'),title.get('title'))
                        naver_news_address.append({'공시대상회사': final_result['공시대상회사'][i],
                                                   '타법인명': final_result['타법인명'][i],
                                                   '뉴스기사제목': title.get('title'), '뉴스기사Url': title.get('href')}) #url 가져오기
                    if len(naver_news_address) > 0 :
                        break
            else:
                # html = 'None'
                naver_news_address.append({'공시대상회사': final_result['공시대상회사'][i],
                                           '타법인명': final_result['타법인명'][i],
                                           '뉴스기사제목': 'None', '뉴스기사Url': 'None'}) #url 가져오기
        return naver_news_address

    def make_dart_data(self):
        
        info_list= self.all_company_info(self.before_week.strftime("%Y%m%d"))
        url_list = []
        d_comp=[]
        for i in range(len(info_list)):
            user_num = i
            rep_url = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo="+info_list['rcp_no'][user_num]
            req = requests.get(rep_url)
            tree = lxml.html.fromstring(req.text)
            onclick = tree.xpath('//*[@id="north"]/div[2]/ul/li[1]/a')[0].attrib['onclick']
            pattern = re.compile("^openPdfDownload\('\d+',\s*'(\d+)'\)")
            dcm_no = pattern.search(onclick).group(1) #각 문서의 내부 dcm_no를 가져와야함
            url_list.append(rep_url)
            if '출자증권양수결정' in info_list['rpt_nm'][user_num]:
                if user_num in info_list[pd.Series(info_list['rpt_nm']).str.contains('기재정정')].index:
                    url_parsing="http://dart.fss.or.kr/report/viewer.do?rcpNo="+info_list['rcp_no'][user_num]+"&dcmNo="+dcm_no+"&eleId=3&offset=3107&length=17182&dtd=dart3.xsd"
                else :
                    url_parsing="http://dart.fss.or.kr/report/viewer.do?rcpNo="+info_list['rcp_no'][user_num]+"&dcmNo="+dcm_no+"&eleId=2&offset=3107&length=17182&dtd=dart3.xsd"
                report=urlopen(url_parsing)
                r=report.read()
                xmlsoup_another=BeautifulSoup(r,'html.parser')
                body=xmlsoup_another.find("body")
                table=body.find_all("table")
                if table[0].select('tr')[0].select('td')[2].select('p'):
                    d_comp.append(table[0].select('tr')[0].select('td')[2].select('p')[0].find_all(text=True)[0].replace(' 주식회사','').replace('주식회사 ',''))
                else:
                    d_comp.append(table[0].select('tr')[0].select('td')[2].find_all(text=True)[0].replace(' 주식회사','').replace('주식회사 ',''))
            else:
                url_parsing= "http://dart.fss.or.kr/report/viewer.do?rcpNo={}&dcmNo={}&eleId=0&offset=0&length=0&dtd=dart3.xsd".format(info_list['rcp_no'][user_num], dcm_no)
                report=urlopen(url_parsing)
                r=report.read()
                xmlsoup_another=BeautifulSoup(r,'html.parser')
                tag_list = xmlsoup_another.select('tbody tr td')
                index = [idx for idx, s in enumerate(tag_list) if '회사명(국적)' in s][0]
                d_comp.append(tag_list[index+1].text.replace(' 주식회사',''))
        info_list['타법인명'] = d_comp
        info_list['문서내용'] = url_list
        info_list.drop(['rcp_no', 'flr_nm', '법인구분'], axis=1, inplace=True)
        final_data=self.get_news_content_keyword(info_list)
        final_data=pd.DataFrame(final_data)
        info_list['뉴스기사제목'] = final_data['뉴스기사제목']
        info_list['뉴스기사Url'] = final_data['뉴스기사Url']
        info_list.fillna('None', inplace=True) #na로 들어가면 구글스프레드시트 업로드시 에러생기므로 'None'으로 항상 바꿔주기
        return info_list
