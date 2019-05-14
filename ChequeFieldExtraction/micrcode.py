import cv2
import numpy as np
import utils
import random
import sys

def get_micrcode(file_name, img_for_extraction_path, dir_path, img):
	# Read the image
	# og_img = cv2.imread(file_name, 0)
	# height, width = og_img.shape[:2]

	# og_img = cv2.resize(og_img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	height, width = img.shape[:2]

	og_image_contours = img

	#utils.display_image('display_image', og_img)

	# Thresholding the image
	(thresh, img_bin) = cv2.threshold(img, 127, 255,cv2.THRESH_BINARY)
	# Invert the image
	# utils.display_image('display_image', img_bin)

	img_bin_inv = 255-img_bin
	# utils.display_image('display_image', img_bin_inv)

	crop_img = img_bin_inv[height - height//6 : ,  : ]
	# utils.display_image('display_image', crop_img)
	print("MICR Code")
	utils.store_img(dir_path, file_name, crop_img, "micrcode")
	#cv2.imwrite( "./temp/" + str(random.randint(0,10000)) + ".jpg", crop_img);

if __name__ == "__main__":
	import utils
	import sys
	import cv2
	import os

	my_path = "./../IDRBT Cheque Image Dataset/300/"
	# filepath = "./samples/"+ str(sys.argv[1])

	store = "./temp/"

	import glob
	onlyfiles = glob.glob(my_path + "*.tif")
	print(onlyfiles)
	i=0
	for filepath in onlyfiles:
		img = cv2.imread(filepath , 0)
		height, width = img.shape[:2]
		img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
		__, filename = os.path.split(filepath)
		get_micrcode(filename, filepath, store, img)
		i+=1