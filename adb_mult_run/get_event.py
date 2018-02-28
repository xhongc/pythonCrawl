from PIL import ImageGrab,ImageChops,Image
now = 'now2'
action = 'action2'

image1 = Image.open('now/60x30/%s.png' % (now))
image2 = Image.open('cature/60x30/%s.png' % (action))
im = ImageChops.difference(image1, image2).getbbox()
print(im)