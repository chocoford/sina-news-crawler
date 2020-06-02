import json
import re
import time, random
import requests
from bs4 import BeautifulSoup
from lxml import etree

urls = []
today = time.strftime("%Y-%m-%d", time.localtime())
with open('url.txt', 'r') as f:
    line = f.readline()
    while line:  
        if 'doc' not in line:
            line = f.readline()
            continue
        if today not in line: 
            line = f.readline()
            continue
        urls.append(line)
        line = f.readline()
random.shuffle(urls)
body_id = {
    "证券": "artibody",
    "新浪娱乐": "artibody",
    "新浪时尚": "artibody",
    "国内财经": "artibody",
    "产经": "artibody",
    "新浪科技": "artibody",
    "新浪体育": "artibody",
    "期货": "artibody",
    "生活": "artibody",
    "新浪手机": "artibody",
    "新浪教育": "artibody",
    "新浪女性": "artibody",
    "债券": "artibody",
    "新浪育儿": "artibody",
    "音乐频道": "artibody",
}

def GetSinaNews(newsurl):
    News = {'url': newsurl}
    bsobj = requests.get(newsurl)
    bsobj.encoding = bsobj.apparent_encoding
    select = BeautifulSoup(bsobj.text, "lxml")
    title = select.find('h1', {"class": "main-title"}).get_text()
    title = title.strip()
    News["title"] = title
    time = select.find('span', {"class": "date"}).get_text()
    time = time.strip()
    t = time[0:10]
    t1 = t[0:4]
    t2 = t[5:7]
    t3 = t[8:]
    t = t1+'/'+t2+'/'+t3
    News['time'] = t
    category = select.find('div', {"class": "channel-path"}).find('a', {})
    if not category:
        category = select.find('div', {"class": "channel-path"})
    category = category.get_text().strip()
    if "债券" in category:
        category = category[:2]
    News['cat'] = category
    print(category)

    content = ''.join([p.get_text() for p in select.find('div', {"class": "article", "id": body_id[category] if category in body_id.keys() else 'article'}).find_all('p', {})])
    News['abstract'] = content[:100] + "..."
    return News



results = []
for url in urls:
    print(url.strip())
    con = GetSinaNews(url.strip()) # 还能用
    results.append(con)
    t = random.random()
    time.sleep(t)
# results.append(GetSinaNews("https://finance.sina.com.cn/money/bond/market/2020-06-02/doc-iircuyvi6229278.shtml")) # 还能用
# results.append(GetSinaNews("https://news.sina.com.cn/w/2020-06-01/doc-iircuyvi6194568.shtml"))





# file = open('test.json', 'w', encoding='UTF-8')
# json.dump(results, file, ensure_ascii=False)
# for l in results:
#     for co in l:
#         print(co)

import dicttoxml
from xml.dom.minidom import parseString
import os
my_item_func = lambda x: x[:-1]

bxml = dicttoxml.dicttoxml(results,custom_root='news', item_func=my_item_func)
xml = bxml.decode('utf-8')

dom = parseString(xml)
prettyxml = dom.toprettyxml(indent='    ')
print(prettyxml)

#将XML字符串保存到文件中。
os.makedirs('files',exist_ok=True)
with open(f'files/sina_news_{today}.xml','w',encoding='utf-8') as f:
    f.write(prettyxml)

