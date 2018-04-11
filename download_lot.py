import urllib.request

def get_yellow(page):
    try:
        url = r"http://mp.window-door-system.com:89/h5/img/tiyan{0}.jpg".format(page)
        path = r"D:\pic\%s.jpg"%page
        data = urllib.request.urlretrieve(url,path)
    except :
        pass

if __name__ == '__main__':

    for page in range(1,51):
        get_yellow(page)