import aircv as ac
import time


def matchImg(imgsrc, imgobj, confidencevalue=0.5):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)

    match_result = ac.find_template(imsrc, imobj,
                                    confidencevalue)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
    print(match_result)
    return match_result


a = time.time()
matchImg(imgsrc=r'c:\test\1.png', imgobj=r'c:\test\1-1.png')
b = time.time()
print(b - a)
