import requests
import re
import urllib.request
import time
import json
import http.cookiejar
from PIL import Image
head ={}
head['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
head['Referer'] = 'http://www.zhihu.com'
head['Host'] = 'www.zhihu.com'
baseurl = 'https://www.zhihu.com/login/phone_num'
url = 'https://www.zhihu.com/'
def getcontent(url):
    head ={}
    head['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    head['Referer'] = 'http://www.zhihu.com'
    head['Host'] = 'www.zhihu.com'
    req = urllib.request.Request(url,headers=head)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    return html
    

def getXSRF(URL):
    content = getcontent(url)
    pattern = re.compile(r'<input type="hidden" name="_xsrf" value="(.+)"/>')
    match = re.findall(pattern,content)
    xsrf = match[0]

    return xsrf

def get_captcha():
    t =str(int(time.time()*1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t +"&type=login"
    image_data = urllib.request.urlopen(captcha_url).read()
    with open('captcha.gif','wb') as f:
        f.write(image_data)

    im = Image.open('captcha.gif')
    
    captcha = input('captcha?\n')
    return captcha
def login(baseurl,phone_num,password):
    login_data ={
        '_xsrf':getXSRF(url),
        'password':password,
        'remember_me':'True',
        'phone_num':phone_num,


    }
    
    

    session = requests.Session()
    
    content = session.post(baseurl,headers=head,data = login_data)
    print (content.text)
    
    s =session.get('http://www.zhihu.com',verify = False,headers=head)
    #print(s.text.encode('utf-8'))
    with open ('zhihu.txt','wb') as f:
        f.write(s.text.encode('utf-8'))

    if (json.loads(content.text))["r"] ==1:
        login_data['captcha'] = get_captcha()
        print(login_data)
        session = requests.Session()
        content = session.post(baseurl,headers=head,data = login_data)
        print (content.text)

        s =session.get('http://www.zhihu.com',verify = False,headers=head)
        with open ('zhihu.txt','wb') as f:
            f.write(s.text.encode('utf-8'))
            
    
    

login(baseurl,'15260959391','chao123456789..')
