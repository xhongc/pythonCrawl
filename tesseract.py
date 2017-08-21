from PIL import Image
import pytesseract
import os

im =Image.open('captcha.jpg')
im = im.convert('RGBA')
pix = im.load()
#print(pix[2,2])
for x in range(im.size[0]):
    for z in range(10):
        pix[x,z] =(255,255,255,255)
        pix[x, im.size[1] - z-1]=(255,255,255,255)
for y in range(im.size[1]):
    for z in range(10):
        pix[z,y]=pix[im.size[0]-1-z,y]=(255,255,255,255)
for y in range(im.size[1]):  # 二值化处理，这个阈值为R=95，G=95，B=95
    for x in range(im.size[0]):
        if pix[x, y][0] < 95 or pix[x, y][1] < 95 or pix[x, y][2] < 95:
            pix[x, y] = (0, 0, 0,255)
        else:
            pix[x, y] = (255, 255, 255,255)
im = im.convert('RGB')
#print(im.size)
im=im.resize((200,100))
im.save('111.jpg')
result = Image.open('111.jpg')
result = pytesseract.image_to_string(result)
result= result.replace('Z','2')
if len(result) == 4:
    print(result)
else:
    print('wrong:%s'%result)
'''import pytesseract
from PIL import Image  # 需要加载PIL库
import os
from numpy import *

img = Image.open('11.jpg')  # PIL库加载图片
img = img.convert('RGB')  # 转换为RGBA
pix = array(img)  # 转换为像素
#print(len(pix))
for y in range(len(pix)):
    for x in range(len(pix[y])):
        if pix[y][x][0]>95:
            pix[y][x]=[255,255,255]
        for z in range(10):
            pix[z][x] = [255,255,255]
            pix[len(pix)-z-1][x]=[255,255,255]
            pix[y][z] = [255,255,255]
            pix[y][len(pix[y])-z-1]=[255,255,255]

#print(pix)
img = Image.fromarray(pix)



img.save('result.jpg')
im = Image.open('result.jpg')
res = pytesseract.image_to_string(im)
print(res)
'''