import cv2
import numpy as np
import utils
import random
import sys

# dir_path = "./temp/"
# img_for_box_extraction_path = str(sys.argv[1]) ##Provide argument as sample/Cheque.tif

# Read the image
def slice_image(og_img):
	# og_img = cv2.imread(img_for_extraction_path, 0)
	# height, width = og_img.shape[:2]

	# og_img = cv2.resize(og_img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	height, width = og_img.shape[:2]

	og_image_contours = og_img

	#utils.display_image('display_image', og_img)

	# Thresholding the image
	(thresh, img_bin) = cv2.threshold(og_img, 160, 255,cv2.THRESH_BINARY)
	# Invert the image
	#utils.display_image('display_image', img_bin)

	img_bin_inv = 255-img_bin
	#utils.display_image('display_image', img_bin_inv)

	crop_img = og_img[height//2 : height - height//6,  : ]
	print("Slice")
	return crop_img
	

def slice_image_get_remaining(og_img):
	# og_img = cv2.imread(img_for_extraction_path, 0)
	height, width = og_img.shape[:2]

	# og_img = cv2.resize(og_img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	# height, width = og_img.shape[:2]

	og_image_contours = og_img

	#utils.display_image('display_image', og_img)

	# Thresholding the image
	(thresh, img_bin) = cv2.threshold(og_img, 160, 255,cv2.THRESH_BINARY)
	# Invert the image
	#utils.display_image('display_image', img_bin)

	img_bin_inv = 255-img_bin
	#utils.display_image('display_image', img_bin_inv)


	crop_img = og_img[height//6 : height - height//6,  : ]
	# utils.display_image('display_image', crop_img)
	# print("Slice_complement")
	return crop_img

if __name__ == "__main__":
	import utils
	import sys
	import cv2
	import os

	my_path = "./../IDRBT Cheque Image Dataset/300/"
	# filepath = "./samples/"+ str(sys.argv[1])

	store = "./temp1/"

	import glob
	onlyfiles = glob.glob(my_path + "*.tif")
	print(onlyfiles)
	i=0
	for filepath in onlyfiles:
		img = cv2.imread(filepath , 0)
		height, width = img.shape[:2]
		img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
		__, filename = os.path.split(filepath)
		sliced_img = slice_image(img)
		utils.display_image('display_image', sliced_img)
		slice_complement_img = slice_image_get_remaining(img)
		utils.display_image('display_image', slice_complement_img)
		i+=1
