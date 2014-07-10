#encoding=utf-8

import requests
from bs4 import BeautifulSoup
from urllib import unquote
import re
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
url = "http://esf.soufun.com/housing/1__1_0_0_0_1_0_0/"
r = requests.get(url)
content = r.content
content = unicode(content, 'gbk').encode('utf-8')
searchFile = open('house1/searchFile.html', 'w')
searchFile.write(content)
searchFile.close()
'''

'''
searchFile = open('house1/searchFile.html', 'r')
content = searchFile.read()
searchFile.close()

soup = BeautifulSoup(content)
houseList = soup.find(id="houselist")
house = houseList.findAll('li')[0]
name = house.find(class_ ='Lname').string
link = house.find(class_ ="iconinfo")['href']
print name, link
'''
# how to get the content from file
link = "http://beijingxiangsuzh.soufun.com/xiangqing/"
r = requests.get(link)
r.encoding = 'gb2312'
content = r.text
soup = BeautifulSoup(content)
lboxList = soup.find_all(class_ = 'lbox', limit = 5)


#detailFile = file('house1/beijingxiangsuzh.txt', 'w')
i = 1
for lbox in lboxList:
    dds = lbox.find_all(['dd', 'dt'])
    
    if dds[0].find(id = 'jjHidden') is not None:
        data = dds[0].find(id = 'jjHidden').text.split('<')[0] 
        print data
        #detailFile.write(data)
    else: 
        for dd in dds:
            if string.find(dd.text, '本段合作编辑者') == -1:
                data = dd.text
                if i != 4 or i != 5:
                    list = data.split('：')
                    data = ''.join(list[1: len(list)])
                print data
                #detailFile.write(data)
                #detailFile.write('\n')
    print 
    i += 1
    #detailFile.write('\n')
#detailFile.close()    

