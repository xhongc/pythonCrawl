import cv2
import numpy as np

# mouse callback function

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 100, (255, 0, 0), -1)


# 创建图像与窗口并将窗口与回调函数绑定
img = np.zeros((500, 500, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while (1):
    cv2.imshow('image', img)
    if cv2.waitKey(1)&0xFF == ord('q'):#按q键退出
        break
cv2.destroyAllWindows()