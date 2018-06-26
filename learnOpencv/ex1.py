import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread(r'd:\test\1.png', 0)

# cv2.imshow('image', img)
# k = cv2.waitKey(0)
# if k == 27:  # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'):  # wait for 's' key to save and exit
#     cv2.imwrite('messigray.png', img)
#     cv2.destroyAllWindows()

plt.imshow(img, cmap='gray', interpolation='bicubic')
plt.xticks([]), plt.yticks([])  # 隐藏X轴和Y轴上的刻度值
plt.show()
