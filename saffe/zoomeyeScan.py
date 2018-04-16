import requests
import json
import configparser
import os

def Login(user, passwd):
    data_info = {'username': user, 'password': passwd}
    data_encoded = json.dumps(data_info)
    respond = requests.post(url='https://api.zoomeye.org/user/login', data=data_encoded)
    conf = configparser.ConfigParser()
    try:
        fp = open('zoom.conf','w')
        fp.close()
        conf.add_section('zoom')
    except:
        print('error')
    conf.read('zoom.conf')

    try:
        r_decoded = json.loads(respond.text)
        access_token = r_decoded['access_token']
        conf.set('zoom','access_token',access_token)
        conf.write(open('zoom.conf','w'))
    except KeyError:
        return '[-] INFO : USERNAME OR PASSWORD IS WRONG, PLEASE TRY AGAIN'
    return access_token


def search(queryType, queryStr, PAGECOUNT, user, passwd,login_sign):
    if login_sign == 'yes':
        headers = {'Authorization': 'JWT ' + Login(user, passwd)}
    else:
        conf = configparser.ConfigParser()
        conf.read('zoom.conf')
        access_token = conf.get('zoom','access_token')
        headers = {'Authorization': 'JWT ' + access_token}

    for i in range(1, int(PAGECOUNT)):
        r = requests.get(url='https://api.zoomeye.org/' + queryType + '/search?query=' + queryStr + '&page=' + str(i),
                         headers=headers)
        response = json.loads(r.text)
        try:
            if queryType == "host":
                for x in response['matches']:
                    print (x['ip'])
            if queryType == "web":
                for x in response['matches']:
                    print (x['ip'][0])
        except KeyError:
            print ("[ERROR] No hosts found")


def main():
    print (" _____                     _____           ____  ")
    print ("|__  /___   ___  _ __ ___ | ____|   _  ___/ ___|  ___ __ _ _ __")
    print ("  / // _ \ / _ \| '_ ` _ \|  _|| | | |/ _ \___ \ / __/ _` | '_ \ ")
    print (" / /| (_) | (_) | | | | | | |__| |_| |  __/___) | (_| (_| | | | |")
    print ("/____\___/ \___/|_| |_| |_|_____\__, |\___|____/ \___\__,_|_| |_|")
    print ("                                |___/                            ")
    login_sign = input('[-] Is this your first login?(eg:yes or no?) ').lower()
    if login_sign == 'yes':
        user = input('[-] PLEASE INPUT YOUR USERNAME:')
        passwd = input('[-] PLEASE INPUT YOUR PASSWORD:')
        Login(user, passwd)
        PAGECOUNT = input('[-] PLEASE INPUT YOUR SEARCH_PAGE_COUNT(eg:10):')
        queryType = input('[-] PLEASE INPUT YOUR SEARCH_TYPE(eg:web/host):')
        queryStr = input('[-] PLEASE INPUT YOUR KEYWORD(eg:tomcat):')
        search(queryType, queryStr, PAGECOUNT, user, passwd, login_sign)
    elif login_sign == 'no':
        print('[+] OK I GET IT ON ACHE')
        user = '1'
        passwd = '1'
        PAGECOUNT = input('[-] PLEASE INPUT YOUR SEARCH_PAGE_COUNT(eg:10):')
        queryType = input('[-] PLEASE INPUT YOUR SEARCH_TYPE(eg:web/host):')
        queryStr = input('[-] PLEASE INPUT YOUR KEYWORD(eg:tomcat):')
        search(queryType, queryStr, PAGECOUNT, user, passwd, login_sign)
    else:
        print('[-] PLEASE Verify that the prams you entered is correct and try again!')

if __name__ == '__main__':
    main()