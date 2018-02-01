import cv2
import numpy as np
from PIL import Image
import os,shutil


class ImageRecognize:
    """
        Image.resize can not  satisfy me ,maybe change another way.
    """

    def __init__(self):
        pass


    @staticmethod
    def __unite_resolution(sourcePath, srcX, srcY, orientation, targetPath,suffix="png"):
        #ImageRecognize.copypng(sourcePath,targetPath)
        img = Image.open(sourcePath)
        size = img.size
        sizes = [size[0], size[1]]

        re_img = None
        if orientation == 1:
            re_img = img.transpose(Image.ROTATE_90)
            temp = sizes[0]
            sizes[0] = sizes[1]
            sizes[1] = temp
            if srcX != size[1] or srcY != size[0]:
                re_img = re_img.resize((srcX, srcY))
        else:
            if srcX != size[0] or srcY != size[1]:
                # tmp = int(float(srcX) / size[0] * size[1])
                re_img = img.resize((srcX, srcY))
        if re_img:
            re_img.save(sourcePath, suffix)
        return sizes

    @staticmethod
    def __image_comparison(templatePath, sourcePath, targetPath, defaultAccurate, defaultMethod="cv2.TM_CCOEFF_NORMED"):
        result = {"match": False, "maxVal": 0, "maxLocX": 0, "maxLocY": 0, "scaleX": 0, "scaleY": 0}
        img_rgb = cv2.imread(sourcePath)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img_template = cv2.imread(templatePath, 0)

        w, h = img_template.shape[::-1]
        method = eval(defaultMethod)
        res = cv2.matchTemplate(img_gray, img_template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # 		print min_val, max_val, min_loc, max_loc
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img_rgb, top_left, bottom_right, (0, 0, 255), 4)
        cv2.imwrite(targetPath, img_rgb)

        result["match"] = max_val >= defaultAccurate
        result["maxVal"] = max_val
        result["maxLocX"] = max_loc[0] + w / float(2)
        result["maxLocY"] = max_loc[1] + h / float(2)
        return result

    @staticmethod
    def img_comparison(templatePath, sourcePath, defaultAccurate=0.5,defaultMethod='cv2.TM_CCOEFF_NORMED'):

        result = {'match': False, 'maxVal': 0, 'maxLocX': 0, 'maxLocY': 0}
        img_rgb = cv2.imread(sourcePath)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img_template = cv2.imread(templatePath, 0)
        method = eval(defaultMethod)
        res = cv2.matchTemplate(img_gray, img_template, method)
        max_val = cv2.minMaxLoc(res)[1]
        result['match'] = max_val >= defaultAccurate
        result['maxVal'] = max_val
        return result

    @staticmethod
    def proxy(templatePath, sourcePath, targetPath, srcX, srcY, orientation=0, defaultAccurate=0.5):
        target_x, target_y = ImageRecognize.__unite_resolution(sourcePath, srcX, srcY, orientation,targetPath)
        result = ImageRecognize.__image_comparison(templatePath, sourcePath, targetPath, defaultAccurate)
        result["maxLocX"] = int(target_x / float(srcX) * result["maxLocX"])
        result["maxLocY"] = int(target_y / float(srcY) * result["maxLocY"])
        result["scaleX"] = target_x / float(srcX)
        result["scaleY"] = target_y / float(srcY)
        return result

    @staticmethod
    def __image_multi_comparison(templatePath, sourcePath, targetPath, defaultAccurate,defaultMethod="cv2.TM_CCOEFF_NORMED"):
        img_rgb = cv2.imread(sourcePath)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(templatePath, 0)
        w, h = template.shape[::-1]

        method = eval(defaultMethod)
        res = cv2.matchTemplate(img_gray, template, method)

        loc = np.where(res >= defaultAccurate)
        print (loc)
        print (zip(*loc[::-1]))
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite(targetPath, img_rgb)

    @staticmethod
    def proxy_multi(templatePath, sourcePath, targetPath, srcX, srcY, orientation=0, defaultAccurate=0.5):
        ImageRecognize.__unite_resolution(sourcePath, srcX, srcY, orientation)
        ImageRecognize.__image_multi_comparison(templatePath, sourcePath, targetPath, defaultAccurate)

if __name__=="__main__":
    moban = r"E:\unity_auto\U3DAutomatorClient\image\source\windows\sample\login.png"
    source = r"E:\unity_auto\U3DAutomatorClient\image\source\windows\sample\source.png"
    result = r"E:\unity_auto\U3DAutomatorClient\image\source\windows\sample\source_result.png"
    print (ImageRecognize.proxy(templatePath=moban, sourcePath=source, targetPath=result,srcX=1680, srcY=1050 ,defaultAccurate=0.5))
