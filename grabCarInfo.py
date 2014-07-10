import requests
import  BeautifulSoup
import sys
import json
from urllib import unquote

file = open('autoSeriesUrl.csv')
url = "http://db.auto.sohu.com/PARA/MODEL/model_para_0000.json"
while 1:
    line = file.readline()
    if not line:
        break
    strlist = line.split('_')
    splitId = strlist[1][0:4]
    targetUrl = url.replace('0000', splitId)
    print targetUrl
    try:
        r = requests.get(targetUrl)
        content = r.content;
        content_re = content.replace('\'', '\"')
        content_json = json.loads(content_re)
        
        for sip_m_trims in content_json["SIP_M_TRIMS"]:
            print sip_m_trims['SIP_T_ID'], ',', content_json['SIP_B_NAME'], ',', content_json['SIP_M_ABBV'], ',', sip_m_trims['SIP_T_YEAR'], ',', unquote(sip_m_trims['SIP_T_NAME'])
            
            
    except:
        print "there is no subbrand in ", splitId 


