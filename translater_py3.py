#coding=utf-8
 
#import httplib
#from json import JSONDecoder
from urllib import parse
import random
import hashlib
import os
import datetime
import requests

#PROXY认证信息
use_proxy = True
#proxy = {"https": "http://域帐号:域密码@devproxy.h3c.com:8080"}
proxy = {"https": "http://""t19525:T123456t""@devproxy.h3c.com:8080"}

#改成你自己腾讯appid及secretKey
appid=20190320000279250  #你的appid
secretKey='r5ALQ0s02v5hPtj1xRvi'  #你的密钥

#文件目录
data_dirs = './data'

#参数设置
fromLang = 'zh'
toLang = 'en'
url = 'https://api.fanyi.baidu.com/api/trans/vip/fieldtranslate'

#发送http请求，调用API
def send_http_request(q):
    salt = random.randint(32768, 65536)
    domain = "electronics"
    sign = str(appid) + q + str(salt) + domain + secretKey
    m1 = hashlib.md5()
    m1.update(bytes(sign, encoding='utf-8'))
    sign = m1.hexdigest()
    
    #发送get请求
    #myurl = url+'?appid='+str(appid)+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    #starttime = datetime.datetime.now()
    #try:
    #    #print(myurl)
    #    if use_proxy:
    #        resp = requests.get(myurl, proxies=proxy, timeout=5)
    #    else:
    #        resp = requests.get(myurl, timeout=5)
    #except Exception:
    #    print(Exception)
    #    print ('requests.get error')
    #    return None
    #
    #endtime = datetime.datetime.now()
    #print((endtime - starttime).seconds)
    
    #发送post请求
    req_dict = {}
    req_dict["appid"] = appid
    req_dict["q"] = q
    req_dict["from"] = fromLang
    req_dict["to"] = toLang
    req_dict["salt"] = salt
    req_dict["sign"] = sign
    req_dict["domain"] = domain
    starttime = datetime.datetime.now()
    try:
        if use_proxy:
            resp = requests.post(url, data=req_dict, proxies=proxy, timeout=5)
        else:
            resp = requests.post(url, data=req_dict, timeout=5)
    except Exception as e:
        print(str(e))
        print('requests.post error')
        return None
        
    endtime = datetime.datetime.now()
    #print((endtime - starttime).seconds)
    
    return resp

#解析回应信息
def resp_cb(resp):
    resp_con = resp.content.decode('utf-8')
    #print(resp_con)
    
    resp_dict = eval(resp_con)
    #resp_dict = JSONDecoder().decode(resp_con)
    #print(json.dumps(resp_dict, ensure_ascii=False, sort_keys=False, indent=4))
    
    if 'error_code' in resp_dict:   
        print('API Failed! '+'error_code:'+str(resp_dict['error_code'])+' error_msg:'+str(resp_dict['error_msg']))
        return ""
        
    result = resp_dict["trans_result"][0]
    print("src: "+result["src"])
    print("dst: "+result["dst"])
    return result["dst"]

#遍历文件
def main():
    for filename in os.listdir(data_dirs):
        if filename.endswith(fromLang):
            fromfile = open(os.path.join(data_dirs, filename), "r", encoding='utf-8')
            tofile = open(os.path.join(data_dirs, filename.replace("."+fromLang, "."+toLang)), "w")
            
            for line in fromfile.readlines():
                response = send_http_request(line.strip())
                if response:
                    target = resp_cb(response)
                    #print(response)
                else:
                    print("something error!!!")
                    fromfile.close()
                    tofile.close()
                    return
                
                if target == "":
                    print("API request error!!!")
                    fromfile.close()
                    tofile.close()
                    return
                
                tofile.write(target+"\n")
                
            fromfile.close()
            tofile.close()

if __name__ == "__main__":
    main()
