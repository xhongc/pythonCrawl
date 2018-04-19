from PIL import Image
import pytesseract
import os

def box():
    path = r"D:\test"
    file = os.listdir(path)[0]
    # print(file)
    im = Image.open(os.path.join(path, file))
    im = im.size
    a = im[0]/413
    b = im[1]/627
    tmp = (a+b)/2
    x = int(146* tmp)
    y = int(548*tmp)
    z = int(266*tmp)
    p = int(575*tmp)
    return (x,y,z,p)

def get_name(file):
    path = r"D:\test"
    img = Image.open(os.path.join(path, file))
    # box = (370,1300,620,1377)
    bbox =(383,1223,608,1283)
    box1 = (261,955,450,995)
    box2 = (350,1313,637,1377)
    #print(img.size)
    boxes = box()
    cropimg = img.crop(boxes)
    cropimg.save(r'D:\zzz.jpg')
    result = Image.open(r'D:\zzz.jpg')
    result = pytesseract.image_to_string(result)
    result = result.replace(' ','')
    result = result.replace('z','2')
    result = result.replace('Z','2')
    result = result.replace('O','0')
    result = result.replace('o','0')
    result = result.replace('l','1').replace("'",'')
    result = result.replace('L','1').replace('T','1')
    result = result.replace('E', '3').replace('I','1')
    result = result.replace('b','6').replace('‘','').replace('’','')
    #print(result)
    return result



def distinct():
    path = r"C:\Users\hongchao\Desktop\erweima"
    list1 = ['254-%s-01' % s for s in range(1, 1001)]
    list2 = ['254-%s-02' % s for s in range(1, 1001)]
    list3 = ['254-%s-03' % s for s in range(1, 1001)]
    lists = list1 + list2 + list3
    # print(lists)
    f = open(r'C:\Users\hongchao\Desktop\que.txt','w',encoding='utf-8')
    for file in os.listdir(path):
        # print(file)
        # print(file.split('.')[0])

        if file.split('.')[0] not in lists:
            f.write(file)
            f.write('\n')

        else:
            lists.remove(file.split('.')[0])
    f.write('\n'.join(lists))
    f.close()

def remove():
    path = r"D:\test"
    with open(r'C:\Users\hongchao\Desktop\que.txt','r') as f:
        for i in f.readlines():

            each = i.replace('\n','')
            if os.path.isfile(os.path.join(path, each)) == True:
                os.remove(os.path.join(path, each))
def rename():

    path = r"D:\test"
    for file in os.listdir(path):
        # print(file)
        if os.path.isfile(os.path.join(path, file)) == True:
            new = get_name(file)
            print(new)
            newname = str(new) + '.jpg'
            try:
                os.rename(os.path.join(path, file), os.path.join(path, newname))
            except:
                os.remove(os.path.join(path, file))
        else:
            pass
if __name__ == '__main__':

    #remove()m
    yes_or_no = input('是否开始对test文件夹重命名 y/n：\n')
    if yes_or_no =='y':
        rename()
    else:
        print('Bye!')
    #distinct()
    #get_name('1516005805428.jpg')
    # box()

    #150,545,265,575