from PIL import ImageChops,Image
image1 = Image.open('action2.png')
image2 = Image.open('now_action.png')
im = ImageChops.difference(image1, image2).getbbox()

print im