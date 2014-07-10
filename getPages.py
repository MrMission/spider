#encode=utf-8
from Queue import Queue
from threading import Thread
from time import sleep, time
from bs4 import BeautifulSoup
from urllib import unquote
import requests
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
        url = url.split('\n')[0]
        q.put(url)
    inFile.close()

def getContent(url):
    r = requests.get(url)
    r.encoding = 'gb2312'
    return r.text
def grabPagesUrl(num, url):
    prefixUrl = 'http://esf.soufun.com'
    content = getContent(url)
    soup = BeautifulSoup(content)
    hlk_next = soup.find(id = 'pagectrol_hlk_next')
    print 'Thread-%d, %s' % (num, url)
    while hlk_next:
        href = prefixUrl + hlk_next['href'] 
        resList.append(href)
        content = getContent(href)
        soup = BeautifulSoup(content)
        hlk_next = soup.find(id = 'pagectrol_hlk_next')
def working(num):
    while 1:
        url = q.get()
        resList.append(url)
        grabPagesUrl(num, url)
        q.task_done()        
def main():
    start = time()
    inFileName = 'house/bj/secondCatalog.txt'
    outFile = open('house/bj/pageUrl.txt', 'w')
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
