from bs4 import BeautifulSoup
import bs4
import pandas as pd
import numpy as np
import time
total_df = pd.DataFrame(columns=["title", "url","case_num", "content"])

file = open('rescue_20191030.txt', 'r', encoding='utf-8')
soup = BeautifulSoup(file, "html.parser")
post = soup.findAll('item')

str1 = """<td height="33" style="padding-left:20px"><img alt="로고" src="/img/hpgonggo/logo_scourt.gif"/></td>"""
str2 = """<td height="27"><img alt="종료" border="0" onclick="window.close();" src="/img/hpgonggo/btn_close.gif" style="cursor:hand"/><img alt="공백" height="10" src="/img/hpgonggo/blank.gif" width="10"/></td>"""

i = 0
for p in post:
    title = p.find('title').text.strip()
    content = p.find('content:encoded').find(text=lambda tag: isinstance(tag, bs4.CData)).string.strip()
    content = content.replace(str1,"").replace(str2,"")
    url = p.find('guid').text
    soup2 = BeautifulSoup(content, "html.parser")
    try:
        code = soup2.findAll('font')[3].text.strip()
    except:
        code = soup2.findAll("span", {"style":"color: 145192; font-size: small;"})[1].text
    print(i,"번째: ",code)
    total_df = total_df.append({"title"    : title,
                                "case_num" : code,
                                "url"      : url,
                                "content"  : content}, ignore_index=True)
    i +=1
total_df.to_excel('./rescue_detail.xlsx', index=False)

def remove_tag(data):
    try:
        soup = BeautifulSoup(data, "html.parser")
        ret = soup.find('a').text.strip()
    except AttributeError:
        ret = data
    return ret

def get_url(data):
    try:
        soup = BeautifulSoup(data, "html.parser")
        ret = soup.find('a')
        url = ret['href']
    except AttributeError:
        url = data
    except TypeError:
        url = data
    return url

def catch_address(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        addr = soup.select('p')[2].text.split('   ')[4].strip()
    except TypeError:
        print(html)
        addr = None
    except IndexError:
        print(soup.select('p')[2])
        addr = None
    return addr


data1 = pd.read_csv('./rescue.csv', engine='python', encoding='utf-8')
data1.shape
data2 = pd.read_excel('./rescue_detail.xlsx')
data1['url'] = data1['subject'].apply(lambda x:get_url(x))
data3 = pd.merge(data1, data2, on=['case_num','url'],how='left')
data3['subject'] = data3['subject'].apply(lambda x:remove_tag(x))
data3['news'] = data3['news'].replace(np.nan, None, regex=True)
data3['news_url'] = data3['news'].apply(lambda x:get_url(x))
data3['news_title'] = data3['news'].apply(lambda x:remove_tag(x))
data3['address'] = data3['content'].apply(lambda x: catch_address(x))

data3.to_excel('./rescue_all.xlsx', index=False)
