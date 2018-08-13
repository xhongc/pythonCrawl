import pytesseract
from PIL import Image

img = Image.open(r'C:\test\100.jpg', 'r')
# img.show()
vcode = pytesseract.image_to_string(img, lang='eng')
print(vcode)
