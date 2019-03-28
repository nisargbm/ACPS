import cv2
import numpy as np
import utils
import random
import sys

def get_signature(img_for_extraction_path, file_name, dir_path, img):
	# Read the image
	# og_img = cv2.imread(file_name, 0)
	# height, width = og_img.shape[:2]

	# og_img = cv2.resize(og_img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	og_img = img
	height, width = og_img.shape[:2]

	#utils.display_image('display_image', og_img)

	x = int(width//3.5)
	y = int(height//2.5)
	new_img = og_img[height - y : height - (height//6), width - x : width]
	#utils.display_image('display_image', new_img)
	height_new, width_new = new_img.shape[:2]


	(thresh, img_bin) = cv2.threshold(new_img, 160, 255,cv2.THRESH_BINARY)
	#utils.display_image('display_image', img_bin)

	img_bin_inv = 255-img_bin
	#utils.display_image('display_image', img_bin_inv)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,1))
	dilated = cv2.dilate(img_bin_inv,kernel,iterations = 3)
	#utils.display_image('display_image', dilated)

	im2, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#utils.display_image('display_image', im2)

	(contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")

	for contour in contours:
		# get rectangle bounding contour
		[x, y, w, h] = cv2.boundingRect(contour)

		# Don't plot small false positives that aren't text
		if w < width//25 or h < height//25:
			continue

		# draw rectangle around contour on original image
		cv2.rectangle(new_img, (x , y), (x + w , y + h), (255, 255, 255), 2)
		crop_img = img_bin[y : y + h, x : x + w]
		utils.display_image('captcha_result', crop_img)
		print("Signature")
		# utils.store_img(dir_path, img_for_extraction_path, crop_img, "signature")

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
		signature.get_signature(filename, filepath, store, img)
		i+=1