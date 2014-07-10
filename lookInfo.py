import requests
import json
url = "http://db.auto.sohu.com/PARA/MODEL/model_para_3964.json"
r = requests.get(url)
content = r.content;
content_re = content.replace('\'', '\"')
content_json = json.loads(content_re)

print content_json["SIP_M_NAME"]

for key in content_json:
    print key, content_json[key]
