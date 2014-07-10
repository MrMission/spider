#encoding=utf-8
from Queue import Queue
from threading import Thread
from time import sleep, time
from bs4 import BeautifulSoup
from urllib import unquote
import requests
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
q = Queue()
resList = []
def initilize(inFileName):
    inFile = open(inFileName, 'r')
    while 1:
        url = inFile.readline()
        if not url:
            break
        q.put(url)
    inFile.close()

def getContent(url):
    while 1:
        r = ''
        try:
            r = requests.get(url)
        except:
            print 'can not download'
            sleep(2)
        if r != '':
            break
    r.encoding = 'gb2312'
    return r.text
def analyze(num, url):
    print 'Thread-', num, q.qsize()
    content = getContent(url)
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

        dh_dh1 = soup.find(class_ = 'dh dh1')
        tags = dh_dh1.find_all('a')
        loc =  tags[3].string
        loc2 = loc[0: len(loc) - 2]

        resList.append(name + ',' +  type + ',' +  loc2 + ','+  location + ',' + address)

def working(num):
    while 1:
        url = q.get()
        analyze(num, url)
        q.task_done()        

def main():
    start = time()
    inFileName = 'house/bj/pageUrl.txt'
    outFile = open('house/bj/bj.txt', 'w')
    initilize(inFileName)
    for i in range(10):
        t = Thread(target = working, args = (i, ))
        t.setDaemon(True)
        t.start()
    q.join()
    for item in resList: 
        outFile.write(item + '\n')
    outFile.close()
    end = time()
    print end - start
main()
