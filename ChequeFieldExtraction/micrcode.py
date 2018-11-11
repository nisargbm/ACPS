import cv2
import numpy as np
import utils
import random
import sys

def get_micrcode(img_for_extraction_path):
	# Read the image
	og_img = cv2.imread(img_for_box_extraction_path, 0)
	height, width = og_img.shape[:2]

	og_img = cv2.resize(og_img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	height, width = og_img.shape[:2]

	og_image_contours = og_img

	utils.display_image('display_image', og_img)

	# Thresholding the image
	(thresh, img_bin) = cv2.threshold(og_img, 160, 255,cv2.THRESH_BINARY)
	# Invert the image
	utils.display_image('display_image', img_bin)

	img_bin_inv = 255-img_bin
	utils.display_image('display_image', img_bin_inv)


	crop_img = og_img[height - height//6 : ,  : ]
	utils.display_image('display_image', crop_img)
	#cv2.imwrite( "./temp/" + str(random.randint(0,10000)) + ".jpg", crop_img);

dir_path = "./temp/"
img_for_extraction_path = str(sys.argv[1]) ##Provide argument as sample/Cheque.tif
get_micrcode(img_for_extraction_path)