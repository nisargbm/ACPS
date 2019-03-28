import boxes
import micrcode
import signature
from slicing import slice_image, slice_image_get_remaining
import underline
import utils
import sys
import cv2
import os

my_path = "./../IDRBT Cheque Image Dataset/300/"
my_sample_path = "./samples/"
# filepath = "./samples/"+ str(sys.argv[1])
# filepath = "./temp/acc/"+ str(sys.argv[1])
# file_path = "./temp/accNum/"

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
	#boxes.find_boxes(filename, filepath, store, img)
	# underline.get_underline(filename, filepath, store, img)
	micrcode.get_micrcode(filename, filepath, store, img)
	i+=1

# onlyfiles = glob.glob(store + "accNum/" + "*.tif")
# print(onlyfiles)
# i=0
# for filepath in onlyfiles:
# 	img = cv2.imread(filepath , 0)
# 	height, width = img.shape[:2]
# 	# img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
# 	__, filename = os.path.split(filepath)
# 	boxes.refine_accNum(filename, store + "accNum/", store, img)
# 	i+=1

# 	# get_micrcode(str(i), f, store)
# 	# get_signature(str(i), f, store)
# 	# get_underline(str(i), f, store)
	# boxes.refine_date(filename, store + "date/", store, img)
	# boxes.refine_accNum(filename, store + "accNum/", store, img)
	# underline.remove_underline_name(filename, filepath, store, img)
	# underline.remove_underline_amount(filename, filepath, store, img)
# 	img = slice_image(f)
# 	utils.display_image('display_image', img)
# 	img = slice_image_get_remaining(f)
# 	utils.display_image('display_image', img)
# 	i+=1


# i=0
# img = cv2.imread(filepath , 0)
# height, width = img.shape[:2]
# # img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
# (thresh, img_bin) = cv2.threshold(img, 160, 255,cv2.THRESH_BINARY)
# # img_bin = 255 - img_bin
# utils.display_image('display_image', img_bin)

# __, filename = os.path.split(filepath)

# print (filename + " -- " + filepath)
# utils.store_img(store, str(99) + filename, img_bin, "boxes_temp")

# boxes.find_boxes(filename, filepath, store, img)
# micrcode.get_micrcode(filename, filepath, store, img)
# signature.get_signature(filename, filepath, store, img)
#underline.get_underline(filename, filepath, store, img)
# sliced_img = slice_image(img)
# utils.display_image('display_image', sliced_img)
# slice_complement_img = slice_image_get_remaining(img)
# utils.display_image('display_image', slice_complement_img)

# boxes.refine_date(filename, store + "date/", store, img)
# boxes.refine_date(filename, filepath, store, img)

# boxes.refine_accNum(filename, store + "accNum/", store, img)
# underline.remove_underline_name(filename, filepath, store, img)
# underline.remove_underline_amount(filename, filepath, store, img)
# dir_path = "./temp/"
# img_for_extraction_path = str(sys.argv[1]) ##Provide argument as sample/Cheque.tif
