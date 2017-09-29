import os
from PIL import Image, ImageChops,ImageDraw,ImageFilter
import array 
import math
import glob
import numpy
from random import shuffle

## Load from and save to
Names ='./test/test-images'
Zip_Names = 'test'

data_image = array.array('B')## type code=unsigned char
data_label = array.array('B')
	
FileList = [] ## pnp 파일 리스트

width =0 
height = 0

for dirname in os.listdir(Names) :
	lable_name = os.path.join(Names,dirname)
	## print(lable_name)
	## os.path.join(path1[,path2[,...]]) ex.'C:\\Python30', 'Script', 'test.py')
	
	for png_name in os.listdir(lable_name):
		if png_name.endswith(".png"):
				FileList.append(os.path.join(Names,dirname,png_name))
	
shuffle(FileList) ## Usefull for further segmenting the validation set


	
for filename in FileList:
	## print(filename)
	label = int(filename.split('\\')[1])
	
	## print(label)
	
	Im = Image.open(filename)
	pixel = Im.load()
	width, height = Im.size
	#print(width)
	#print(height)
	
	for x in range(0,width):
		for y in range(0,height):
			#height-> index range error -> 해결
			#print(type(pixel[y,x]))
			if type(pixel[y,x]) == int :
			## python an integer is required (got type tuple) error 발생
			## int 값 ?이 append되다가 한번씩
			## -> 끝에[?,255]로 튜플값이 들어가버림
			## 그래서 0번째 값을 지정해줘야 함
				data_image.append(pixel[y,x])
			elif type(pixel[y,x]) == tuple : 
				#print(filename)
				#print(label)
				#print(width)
				#print(height)
				#print(pixel[y,x])
				#print(pixel[y,x][0])
				#print(type(pixel[y,x]))
				data_image.append(pixel[y,x][0])
			#data_image.append(Im.getpixel((y,x)))

data_label.append(label) # labels start (one unsigned byte each)
			
hexval = "{0:#0{1}x}".format(len(FileList),6) # number of files in HEX

# header for label array
header = array.array('B')
header.extend([0,0,8,1,0,0])
header.append(int('0x'+hexval[2:][:2],16))
header.append(int('0x'+hexval[2:][2:],16))

data_label = header + data_label
# additional header for images array
if max([width,height]) <= 256:
	header.extend([0,0,0,width,0,0,0,height])
else:
	raise ValueError('Image exceeds maximum size: 256x256 pixels');

header[3] = 3 # Changing MSB for image data (0x00000803)
	
data_image = header + data_image

output_file = open(Zip_Names+'-images-idx3-ubyte', 'wb')
data_image.tofile(output_file)
output_file.close()

output_file = open(Zip_Names+'-labels-idx1-ubyte', 'wb')
data_label.tofile(output_file)
output_file.close()

# gzip resulting files
os.system('gzip '+Zip_Names+'-images-idx3-ubyte')
os.system('gzip '+Zip_Names+'-labels-idx1-ubyte')
