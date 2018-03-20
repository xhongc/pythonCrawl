from PIL import Image

img = Image.open('25.jpg')#466,747
a = 2.3176
box = (123*a,240*a,343*a,465*a)
croping = img.crop(box)
croping.save('12.jpg')
print(a)
# os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')