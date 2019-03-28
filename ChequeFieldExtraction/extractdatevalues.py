import utils
import sys
import cv2
import os
import numpy as np

def extract_boxes(file_name, img_for_extraction_path, dir_path, img):
	folder_name = filename.split(".")[0]
	store_loc = dir_path + "date_segmented3/"
	print (store_loc)
	height, width = img.shape[:2]
	print(width)
	delta = (width//100) 
	digit_width = (width//8)
	temp = None
	for i in range(0,8):
		if i is 0:
			output_image = img[ height//20 : height - (height//20), delta : ((i+1)*digit_width) - delta]
			h, w = output_image.shape[:2]
			# utils.display_image("image", output_image)
			gap_x = w//6
			gap_y = h//6
			vis = np.zeros((h + (2*gap_y), w + (2*gap_x)), np.uint8)
			vis[gap_y : gap_y + h, gap_x : gap_x + w] = output_image
			output_image = vis
			# utils.display_image("image", output_image)
			kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
			output_image = cv2.dilate(output_image, kernel, iterations=2)
			# utils.display_image("image", output_image)
			output_image = cv2.resize(output_image, (28, 28), interpolation = cv2.INTER_AREA)
			# utils.display_image("image", output_image)
			amount_image = output_image
			utils.store_img(store_loc, "position_" + str(i) + ".tif", output_image , folder_name)
		elif i is 7:
			output_image = img[ height//20 : height - (height//20), (i * digit_width) + delta : width - delta]
			h, w = output_image.shape[:2]
			# utils.display_image("image", output_image)
			gap_x = w//6
			gap_y = h//6
			vis = np.zeros((h + (2*gap_y), w + (2*gap_x)), np.uint8)
			vis[gap_y : gap_y + h, gap_x : gap_x + w] = output_image
			output_image = vis
			# utils.display_image("image", output_image)
			kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
			output_image = cv2.dilate(output_image, kernel, iterations=2)
			# utils.display_image("image", output_image)
			output_image = cv2.resize(output_image, (28, 28), interpolation = cv2.INTER_AREA)
			# utils.display_image("image", output_image)
			crop_img = output_image
			h1, w1 = amount_image.shape[:2]
			h2, w2 = crop_img.shape[:2]
			vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
			vis[:h1, :w1] = amount_image
			vis[:h2, w1:w1+w2] = crop_img
			amount_image = vis
			utils.store_img(store_loc, "position_" + str(i) + ".tif", output_image , folder_name)
		else:
			output_image = img[ height//20 : height - (height//20) , (i * digit_width) + delta : ((i+1)*digit_width) - delta]
			h, w = output_image.shape[:2]
			gap_x = w//6
			gap_y = h//6
			vis = np.zeros((h + (2*gap_y), w + (2*gap_x)), np.uint8)
			vis[gap_y : gap_y + h, gap_x : gap_x + w] = output_image
			output_image = vis
			kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
			output_image = cv2.dilate(output_image, kernel, iterations=2)
			output_image = cv2.resize(output_image, (28, 28), interpolation = cv2.INTER_AREA)
			# utils.display_image("image", output_image)
			utils.store_img(store_loc, "position_" + str(i) + ".tif", output_image , folder_name)
			crop_img = output_image
			h1, w1 = amount_image.shape[:2]
			h2, w2 = crop_img.shape[:2]
			vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
			vis[:h1, :w1] = amount_image
			vis[:h2, w1:w1+w2] = crop_img
			amount_image = vis
	# utils.display_image("image", amount_image)
		# h1, w1 = amount_image.shape[:2]
		# h2, w2 = crop_img.shape[:2]
		# vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
		# vis[:h1, :w1] = amount_image
		# vis[:h2, w1:w1+w2] = crop_img
		# amount_image = vis

def extract_boxes1(file_name, img_for_extraction_path, dir_path, img):
	folder_name = filename.split(".")[0]
	store_loc = dir_path + "date_segmented3/"
	print (store_loc)
	height, width = img.shape[:2]
	print(width)
	delta = (width//100) 
	digit_width = (width//8)
	temp = None
	for i in range(0,9):
		if i is 0:
			img[ : height//20, :] = 0
			img[ height - (height//20) : , :] = 0
			img[ : , 0 : delta] = 0
			# utils.display_image("image", img)
			# utils.store_img(store_loc, "position_" + str(i) + ".tif", output_image , folder_name)
		elif i is 8:
			img[ : , (i * digit_width) - delta : ] = 0
			# utils.display_image("image", img)
		else:
			img[ : , (i * digit_width) - delta : ((i)*digit_width) + delta] = 0
			# utils.display_image("image", img)
	# utils.display_image("image", img)
	# utils.display_image("image", horizontal_lines_img)
	extract_boxes(filename, img_for_extraction_path, dir_path, img)

if __name__ == "__main__":

	my_path = "./temp1/date9/"
	store = "./temp1/"

	import glob
	onlyfiles = glob.glob(my_path + "*.tif") # Cheque 100831.tif
	len(onlyfiles)
	print(onlyfiles)
	i=0
	for filepath in onlyfiles:
		img = cv2.imread(filepath , 0)
		__, filename = os.path.split(filepath)
		extract_boxes1(filename, filepath, store, img)
		i+=1

	# import argparse
	# ap = argparse.ArgumentParser()
	# # ap.add_argument("-i", "--image", required=True,
	# # 	help="path to input image")
	# ap.add_argument("-i", "--image", required=True,
	# 	help="image path")
	# args = vars(ap.parse_args())

	# filepath = args["image"]
	# img = cv2.imread(filepath , 0)
	# __, filename = os.path.split(filepath)
	# extract_boxes(filename, filepath, store, img)