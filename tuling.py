#!/usr/bin /env python
# -*- coding :utf8 -*-

import json
import urllib.request


from ymlhandle import cfg

def tuling(txt):
    api_url = cfg['tuling']['url']
    req = {
    "perception":
    {
        "inputText":
        {
            "text": txt
        },

        "selfInfo":
        {
            "location":
            {
                "city": "南京",
                "province": "江苏",
                "street": "XXX"
            }
        }
    },
    "userInfo": 
    {
        "apiKey": cfg['tuling']['apiKey'],
        "userId": cfg['tuling']['userId']
    }
    }
    req = json.dumps(req).encode('utf8')
    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    res = response.read().decode('utf8')
    response_dic = json.loads(res)
    results_text = response_dic['results'][0]['values']['text']
    return results_text

if __name__ == '__main__':
    print(tuling('你好吗'))