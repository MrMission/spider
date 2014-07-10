#encoding=utf-8
from Queue import Queue
from threading import Thread
from time import sleep, time
from bs4 import BeautifulSoup
from urllib import unquote
import requests
import string
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
q = Queue()
resList = []
firstList = []
secondList = []
thirdList = []
#get pageUrls
def grabFirst(url):
    regex = r'(.*)/housing.*'
    p = re.compile(regex)
    m = p.search(url)
    prefixUrl = m.group(1)

    regex = r'.*esf.(.*).soufun.*'
    p = re.compile(regex)
    m = p.search(url)
    add = m.group(1)

    content = getContent(url)
    soup = BeautifulSoup(content)
    hlist_21 = soup.find(id = 'hlist_21')
    tags = hlist_21.find_all('a')
    for index, tag in enumerate(tags):
        if index == 0:
            continue
        href = prefixUrl + tag['href']
        firstList.append(href)
    #test
    file = open('house/' + add + '/fist.txt', 'w')
    for item in firstList:
        file.write(item + '\n')
    file.close()
    print 'write into firstList successfully.'

def grabSecond():
    for url in firstList:
        #get prefixUrl
        regex = r'(.*)/housing.*'
        p = re.compile(regex)
        m = p.search(url)
        prefixUrl = m.group(1)

        content = getContent(url)
        soup = BeautifulSoup(content)
        shangquan = soup.find(class_ = 'shangquan')
        tags = shangquan.find_all('a')
        for index, tag in enumerate(tags):
            if index == 0:
                continue
            href = prefixUrl + tag['href']
            secondList.append(href)
    regex = r'.*esf.(.*).soufun.*'
    p = re.compile(regex)
    m = p.search(url)
    add = m.group(1)
    file = open('house/' + add + '/second.txt', 'w')
    for item in secondList:
        file.write(item + '\n')
    file.close()
    print 'write into secondList successfully!'

def grabPage():
    for url in secondList:
        print url
        regex = r'(.*)\d+_0_0/'
        p = re.compile(regex)
        m = p.search(url)
        preUrl = m.group(1)
        postUrl = '_0_0/'
        content = getContent(url)
        soup = BeautifulSoup(content)
        try:
            fy_text = soup.find(class_ = 'fy_text').string
        except:
            continue
        num = int(fy_text.split('/')[1])
        for i in range(1, num + 1):
            url = preUrl + str(i) + postUrl
            thirdList.append(url)
    regex = r'.*esf.(.*).soufun.*'
    p = re.compile(regex)
    m = p.search(url)
    add = m.group(1)
    # test
    file = open('house/' + add + '/page.txt', 'w')
    for item in thirdList:
        file.write(item + '\n')
    file.close()
    print 'write into page successfully!'
    
def initilize(url):
    regex = r'.*esf.(.*).soufun.*'
    p = re.compile(regex)
    m = p.search(url)
    add = m.group(1)
    inFileName = 'house/' + add + '/page.txt'
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
    # 把这个url改成广州的就可以直接下广州的
    urlList = ['http://esf.suzhou.soufun.com/housing/', 'http://esf.nn.soufun.com/housing/', 'http://esf.cd.soufun.com/housing/', 'http://esf.hz.soufun.com/housing/']
    for url in urlList:
        regex = r'.*esf.(.*).soufun.*'
        p = re.compile(regex)
        m = p.search(url)
        add = m.group(1)
        print add

        resList = []
        firstList = []
        secondList = []
        thirdList = []

        grabFirst(url)
        grabSecond()
        grabPage()
        initilize(url)
        outFile = open('house/' + add + '.txt', 'w')
        for i in range(10):
            t = Thread(target = working, args = (i, ))
            t.setDaemon(True)
            t.start()
        q.join()
        for item in resList: 
            print item
            outFile.write(item + '\n')
        outFile.close()
        print add + 'finish'
    end = time()
    print end - start
main()
