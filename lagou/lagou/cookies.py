import requests
import json
import base64

def get_cookies(account,password):
    loginurl ="https://passport.lagou.com/login/login.html"
    password = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    post_data = {
        "isValidate": "true",
        "username": account,
        "password": password,


    }

    session = requests.Session()
    headers={
        "Use-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"
    }
    r = session.post(loginurl,data=post_data,headers=headers)
    print(r.content)
    info = json.loads(r.content.decode('utf-8'))

    if info["retcode"] == "0":
        print("suceess cookie")
        cookie = session.cookies.get_dict()
        return json.dumps(cookie)
    else:
        print('Error')
if __name__ =='__main__':
    get_cookies("15260959391","chao123456789..")