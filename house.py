#encoding=utf-8
import requests
import string
from bs4 import BeautifulSoup
import re
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

urlPrefix = 'http://esf.soufun.com'

def getLocalList(url):
    localListFile = open('house1/localList.txt', 'w')
    r = requests.get(url)
    r.encoding = 'gb2312'
    content = r.text
    soup = BeautifulSoup(content)
    hlist_21 = soup.find(id = 'hlist_21')
    locationList = hlist_21.find_all('a')
    for location in locationList:
        locName = location.text
        if string.find(locName, '不限') == -1:
            locurl = urlPrefix + location['href']
            localListFile.write(locurl)
            localListFile.write('\n')
            '''
            number = int(soup.find(class_='number orange').text)
            if number > 2000:
                print 'warning:', locName, locurl, number 
            '''
    localListFile.close()

#urlListFile = open('house1/urlList.txt', 'w')
def getPageList():
    localListFile = open('house1/localList.txt', 'r')
    pageListFile = open('house1/pageList.txt', 'w')
    while 1:
        count = 1
        localUrl = localListFile.readline()
        pageListFile.write(localUrl)
        if not localUrl:
            break
        r = requests.get(localUrl)
        r.encoding = 'gb2312'
        content = r.text
        soup = BeautifulSoup(content)
        hlk_next = soup.find(id = 'pagectrol_hlk_next')
        while (hlk_next is not None):
            count += 1
            nextUrl = urlPrefix + hlk_next['href']
            pageListFile.write(nextUrl + '\n')
            r = requests.get(nextUrl)
            r.encoding = 'gb2312'
            content = r.text
            soup = BeautifulSoup(content)
            hlk_next = soup.find(id = 'pagectrol_hlk_next')
        print localUrl, count
        # exactly it's not enough!
        if count >= 100:
            print 'warning:', localUrl
    localListFile.close()
    pageListFile.close()

def getDetailUrlList():
    pageListFile = open('house1/pageList.txt', 'r')
    detailUrlListFile = open('house1/detailUrlList.txt', 'w')
    count = 0
    while 1:
        count += 1
        pageUrl = pageListFile.readline()
        print pageUrl, count
        if not pageUrl:
            break
        r = requests.get(pageUrl)
        r.encoding = 'gb2312'
        content = r.text
        soup = BeautifulSoup(content)
        details = soup.find_all(class_='iconinfo')
        for detail in details:
            #print detail['href']
            detailUrlListFile.write(detail['href'] + '\n')
    pageListFile.close()
    detailUrlListFile.close()

def getDetailList():
    detailUrlListFile = open('house1/detailUrlList.txt', 'r')
    detailListFile = open('house1/detailList.txt', 'a')
    count = 0
    while 1:
        result = {}
        count += 1
        detailUrl = detailUrlListFile.readline()
        #print detailUrl, count
        if not detailUrl:
            break
        r = requests.get(detailUrl)
        r.encoding = 'gb2312'
        content = r.text
        soup = BeautifulSoup(content)
        lboxList = soup.find_all(class_ = 'lbox', limit = 5)
        yihang = soup.find_all(class_ = 'yihang', limit = 5)
        try:
            for index, lbox in enumerate(lboxList):
                key = yihang[index].text[0: 4]
                if (string.find(key, '基本信息') != -1):
                    print 'a',
                    dds = lbox.find_all(['dd', 'dt'])
                    dic = {}
                    for dd in dds:
                        if string.find(dd.text, '本段合作编辑者') == -1:
                            resList = dd.text.split('：')
                            dic[resList[0]] = resList[1]
                    result[key] = dic
                            #detailListFile.write(data + '\n')
                elif (string.find(key, '配套设施') != -1):
                    print 'b',
                    dds = lbox.find_all(['dd', 'dt'])
                    dic = {}
                    for dd in dds:
                        if string.find(dd.text, '本段合作编辑者') == -1:
                            resList = dd.text.split('：')
                            dic[resList[0]] = resList[1]
                    result[key] = dic
                            #detailListFile.write(data + '\n')
                elif (string.find(key, '小区简介') != -1):
                    print 'c',
                    dd = lbox.find(['dt'])
                    data = ''
                    if dd.find(id = 'jjHidden') is not None:
                        data = dd.find(id = 'jjHidden').text.split('<')[0]
                    else:
                        data = dd.text
                    result[key] = data
                    #detailListFile.write(data + '\n')
                
                elif (string.find(key, '交通状况') != -1):
                    print 'd',
                    dds = lbox.find(['dd', 'dt'])
                    result[key] = dds.text
                    #detailListFile.write(data + '\n')
                elif (string.find(key, '周边信息') != -1):
                    print 'e'
                    dds = lbox.find_all(['dd', 'dt'])
                    dic = {}
                    for dd in dds:
                        if string.find(dd.text, '本段合作编辑者') == -1:
                            resList = dd.text.split('：')
                            dic[resList[0]] = resList[1]
                    result[key] = dic
                            #detailListFile.write(data + '\n')
            resJson = json.dumps(result, sort_keys = True)
            detailListFile.write(resJson)
            #print resJson
        except:
            s = sys.exc_info()
            print detailUrl, count
            print 'Error "%s" happened on line %d' % (s[1],s[2].tb_lineno)
        detailListFile.write('\n')  

    detailUrlListFile.close()
    detailListFile.close()

url = 'http://esf.soufun.com/housing/__1_0_0_0_1_0_0/'
#getLocalList(url)
#getPageList()
#getDetailUrlList()
getDetailList()


