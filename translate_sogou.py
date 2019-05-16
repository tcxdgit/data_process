#!/usr/bin/python
import requests
import hashlib
import urllib.parse


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

proxy = {"https": "http://""t19525:T123456t""@devproxy.h3c.com:8080"}
url = "http://fanyi.sogou.com:80/reventondc/api/sogouTranslate"
pid = "570d8af90c7fe6fe7128b003a3253574"
salt = "1508404016012"
q = "你好"
sign = md5(pid+q+salt+"47e399aedc8424a00914c98342595beb")
print(sign)

#in the case, the pid with the key counts sign will be in this.
# sign = "882e9c08aba3b673d055a6d1a14d0c9f"

payload = "from=zh-CHS&to=en&pid=" + pid + "&q=" + urllib.parse.quote(q) + "&sign=" + sign + "&salt=" + salt
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'accept': "application/json"
    }
response = requests.request("POST", url, data=payload, headers=headers, proxies=proxy, timeout=5)
# response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
# print(response.content)


# resp_dict = eval(response.text)

# print(resp_dict)
