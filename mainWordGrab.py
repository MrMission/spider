#encoding=utf-8
import requests
import string
from threading import Thread
from Queue import Queue
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def grabFirstCatalog(url, prefixUrl, fileName):
    firstCatalogFile = open(fileName, 'w')
    r = requests.get(url)
    r.encoding = 'gb2312'
    content = r.text
    soup = BeautifulSoup(content)
    hlist_21 = soup.find(id = 'hlist_21')
    tags = hlist_21.find_all('a')
    for index, tag in enumerate(tags):
        if index == 0:
            continue
        href = prefixUrl + tag['href']
        firstCatalogFile.write(href + '\n')
    firstCatalogFile.close()    
    print 'write into firstCatalogFile successfully.'

def grabSecondCatalog(inFile, prefixUrl, outFile):
    firstCatalogFile = open(inFile, 'r')
    secondCatalogFile = open(outFile, 'w')
    while 1:
        url = firstCatalogFile.readline()
        if not url:
            break
        r = requests.get(url)
        r.encoding = 'gb2312'
        content = r.text
        soup = BeautifulSoup(content)
        shangquan = soup.find(class_ = 'shangquan')
        tags = shangquan.find_all('a')
        for index, tag in enumerate(tags):
            if index == 0:
                continue
            href = prefixUrl + tag['href']
            secondCatalogFile.write(href + '\n')
    firstCatalogFile.close()
    secondCatalogFile.close()
    print 'write into secondCatalogFile successfully!'
q = Queue()
def grabPages(url):
    prefixUrl = 'http://esf.sh.soufun.com'
    while 1:
        r = requests.get(url)
        r.encoding = 'gb2312'
        content = r.text
        soup = BeautifulSoup(content)
        hlk_next = soup.find(id = 'pagectrol_hlk_next')
        while hlk_next:
            href = prefixUrl + hlk_next['href'] 
            #outFile.write(href + '\n')
            #print href
            r = requests.get(href)
            r.encoding = 'gb2312'
            content = r.text
            soup = BeautifulSoup(content)
            hlk_next = soup.find(id = 'pagectrol_hlk_next')
    print 'write into pagesFile successfully!'
def working():
    while True:
        url = q.get()
        grabPages(url)
        q.task_done()

def main():
    #pagesFile = 'house/sh/pagesFile.txt'
    for i in range(2):
        t = Thread(target=working)
        t.setDaemon(True)
        t.start()
    inFileName = 'house/sh/test.txt'
    inFile = open(inFileName, 'r')
    while 1:
        url = inFile.readline()
        if not url:
            break
        q.put(url)
    inFile.close()
    q.join()

#main()
        
def analyze(inFileName, outFileName):
    inFile= open(inFileName, 'r')
    outFile = open(outFileName, 'w')
    count = 1
    while 1:
        if count % 50 == 1:
            print count
        count += 1
        url = inFile.readline()
        if not url:
            break
        try:
            r = requests.get(url)
            r.encoding = 'gb2312'
            content = r.text
            soup = BeautifulSoup(content)
            houseList = soup.find(id = 'houselist')
            liList = houseList.find_all('li')
            for li in liList:
                dt = li.find('dt')
                img = dt.find('img')['src']
                if string.find(img, 'bieshu.jpg') != -1:
                    type = '别墅'
                elif string.find(img, 'zhuzhai1.gif') != -1:
                    type = '住宅'
                elif string.find(img, 'shangpu.jpg') != -1:
                    type = '商铺'
                elif string.find(img, 'xiezilou.jpg') != -1:
                    type = '写字楼'
                else:
                    continue
                name = dt.find('a').text
                
                rawLoc = dt.find('span')
                if rawLoc:
                    rawLoc1 = rawLoc.text
                    location = rawLoc1[1: len(rawLoc1) - 1]
                else:
                    location = ''
                address = dt.text.split(']')[1]
                outFile.write(name + ',' +  type + ',' +  location + ',' + address + '\n')
            
        except:
            s = sys.exc_info()
            print url
            print 'Error "%s" happened in line %d' % (s[1], s[2].tb_lineno)
            inFile.close()
            outFile.close()
            break
    print 'write into result successfully!'

'''
# sh
url = 'http://esf.sh.soufun.com/housing/__0_0_0_0_1_0_0/'
prefixUrl = 'http://esf.sh.soufun.com'
firstCatalogFile = 'house/sh/firstCatalog.txt'
secondCatalogFile = 'house/sh/secondCatalog.txt'
pagesFile = 'house/sh/pagesFile.txt'
shFile = 'house/sh.csv'
#grabFirstCatalog(url, prefixUrl, firstCatalogFile)
#grabSecondCatalog(firstCatalogFile, prefixUrl, secondCatalogFile)
#grabPages(secondCatalogFile, prefixUrl, pagesFile)
#analyze(pagesFile, shFile)
'''
# bj
url = 'http://esf.soufun.com/housing/__0_0_0_0_1_0_0/'
prefixUrl = 'http://esf.soufun.com'
firstCatalogFile = 'house/bj/firstCatalog.txt'
secondCatalogFile = 'house/bj/secondCatalog.txt'
pagesFile = 'house/bj/pagesFile.txt'
shFile = 'house/bj.csv'
#grabFirstCatalog(url, prefixUrl, firstCatalogFile)
grabSecondCatalog(firstCatalogFile, prefixUrl, secondCatalogFile)
#grabPages(secondCatalogFile, prefixUrl, pagesFile)
#analyze(pagesFile, shFile)
'''
# gz, sz,  
url = 'http://esf.gz.soufun.com/housing/__0_0_0_0_1_0_0/'
prefixUrl = 'http://esf.gz.soufun.com'
firstCatalogFile = 'house/gz/firstCatalog.txt'
secondCatalogFile = 'house/gz/secondCatalog.txt'
pagesFile = 'house/gz/pagesFile.txt'
shFile = 'house/gz.csv'
grabFirstCatalog(url, prefixUrl, firstCatalogFile)
grabSecondCatalog(firstCatalogFile, prefixUrl, secondCatalogFile)
grabPages(secondCatalogFile, prefixUrl, pagesFile)
analyze(pagesFile, shFile)
'''
