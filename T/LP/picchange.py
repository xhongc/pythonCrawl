#!/usr/bin/env python
# encoding: utf-8
import os,shutil
import os.path
from PIL import Image
class picchange():
	def __init__(self,path,xo,yo,xn,yn):
		self.alterpath(path,xo,yo,xn,yn)

	def alterpath(self,path,xo,yo,xn,yn):
		filelist = os.listdir(path)
		for files in filelist:
			filepath = os.path.join(path, files)
			if filepath.endswith(str(xn)+"x"+str(yn)):
				for item in os.listdir(filepath):
					itempath = os.path.join(filepath, item)
					os.remove(itempath)
				os.removedirs(filepath)
		for files in filelist:
			if files.endswith(str(xo)+"x"+str(yo)):
				str1 = (path + os.sep + files).decode("utf-8").encode("gb2312")
				str2 = (path + os.sep + files.split(str(xo)+"x"+str(yo))[0] + str(xn)+"x"+str(yn)).decode("utf-8").encode("gb2312")
				shutil.copytree(str1, str2)
				self.rename(str2,xo,yo,xn,yn)

	def rename(self,path,xo,yo,xn,yn):
		filelist = os.listdir(path)
		for files in filelist:
			if files.endswith(".png"):
				Olddir = os.path.join(path, files)
				im = Image.open(Olddir)
				(x, y) = im.size
				x_s = x *(float(xn)/float(xo))
				y_s = y * (float(yn)/float(yo))
				out = im.resize((int(x_s), int(y_s)), Image.ANTIALIAS)
				out.save(Olddir)

	print ("OK")
if __name__ == "__main__":
	path=r"D:\STAF\samples\java\script\qatest\data\script\case"
	picchange(path,1080,1920,1536,2560)
	picchange(path,1080,1920,540,960)
	picchange(path,1080,1920,480,854)
	picchange(path,1080,1920,480,800)
	picchange(path,1080,1920,750,1334)
	picchange(path,1080,1920,768,1280)
	picchange(path,1080,1920,800,1280)
	picchange(path,1080,1920,1024,768)
	picchange(path,1080,1920,1080,1800)
	picchange(path,1080,1920,720,1280)
	picchange(path,1080,1920,1080,2040)
	picchange(path,1080,1920,1920,1080)
	picchange(path,1080,1920,2048,1536)
	picchange(path,1080,1920,2560,1600)
	picchange(path,1080,1920,2732,2048)
	picchange(path,1080,1920,1440,2960)