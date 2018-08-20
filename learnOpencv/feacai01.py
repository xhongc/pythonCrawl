import cv2

filepath = r"C:\test\cham.jpg"
img = cv2.imread(filepath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

classifier = cv2.CascadeClassifier(
    r'C:\Users\xhongc\work\model\opencvdata\data\haarcascades\haarcascade_frontalface_default.xml')
color = (0, 255, 0)

faceRects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
print(faceRects)
if len(faceRects):
    for faceRect in faceRects:  # 单独框出每一张人脸
        x, y, w, h = faceRect

        # 框出人脸
        cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
        # 左眼
        cv2.circle(img, (x + w // 4, y + h // 4 + 30), min(w // 8, h // 8),
                   color)
        # 右眼
        cv2.circle(img, (x + 3 * w // 4, y + h // 4 + 30), min(w // 8, h // 8),
                   color)
        # 嘴巴
        cv2.rectangle(img, (x + 3 * w // 8, y + 3 * h // 4),
                      (x + 5 * w // 8, y + 7 * h // 8), color)
cv2.imshow("image", img)  # 显示图像
c = cv2.waitKey(10)

cv2.waitKey(0)
cv2.destroyAllWindows()
