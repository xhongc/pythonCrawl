import threading
def ppap():
    i=1
    while 1:
        i+=1
        print(i)
        if i ==25:
            print('gggg')
            break

for t in range(5):
    t = threading.Thread(target=ppap,name=t)
    t.start()