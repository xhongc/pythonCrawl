import cv2
import numpy as np

# 当鼠标按下时为True
drawing = False
# 如果mode为true时绘制矩形，按下'm'变成绘制曲线
mode = True
ix, iy = -1, -1


# 创建回调函数
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode
    # 当按下左键时返回起始位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    # 当左键按下并移动时绘制图形，event可以查看移动，flag查看是否按下
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing == True:
            if mode == True:
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
            else:
                # 绘制圆圈，小圆点连在一起就成了线，3代表笔画的粗细
                cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

    # 当鼠标松开时停止绘图
    elif event == cv2.EVENT_LBUTTONUP:
        drawing == False


'''
下面把回调函数与OpenCV窗口绑定在一起，在主循环中奖'm'键与模式转换绑定在一起
'''
img = np.zeros((500, 500, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)
while (1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1)
    if k == ord('m'):
        mode = not mode
    elif k == ord('q'):
        break
cv2.destroyAllWindows()