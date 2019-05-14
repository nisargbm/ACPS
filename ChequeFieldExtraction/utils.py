import numpy as np
import argparse
import cv2
import os
 
def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
 
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
 
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def sort_contours_area(cnts):
	cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x), reverse = True)
	return cntsSorted

def display_image(imageName, image):
	cv2.imshow(str(imageName), image)
	cv2.waitKey()

def display_image1(image, imageName = 'image'):
	cv2.imshow(str(imageName), image)
	cv2.waitKey()

def store_img(dir_path, filename, img_to_store, type_of_image):
	full_path = dir_path + "/" + type_of_image + "/" 
	create_dir(full_path)
	cv2.imwrite(full_path + filename, img_to_store)
	
def create_dir(full_path):
	if not os.path.exists(full_path):
		os.makedirs(full_path)

def find_overlap(image, values1, values2):
	height, width = image.shape[:2]
	ref = np.zeros((height,width),dtype=np.int)
	src1 = ref.copy() 
	src2 = ref.copy()
	x1 = values1[0]
	y1 = values1[1]
	w1 = values1[2]
	h1 = values1[3]
	x2 = values2[0]
	y2 = values2[1]
	w2 = values2[2]
	h2 = values2[3]
	# display_image1(image[y1 - (height // 12): y1 + h2 + (height // 100), x1 : x1+w1])
	# display_image1(image[y2 - (height // 12): y2 + h2 + (height // 100), x2 : x2+w2])
	src1[y1 - (height // 12): y1 + h2 + (height // 100), x1 : x1+w1] = 1
	# display_image1(src1)
	src2[y2 - (height // 12): y2 + h2 + (height // 100), x2 : x2+w2] = 1
	overlap1 = src1+src2
	overlap2 = overlap1.copy()
	# print(overlap1)
	overlap1[overlap1 == 1] = 0
	overlap1[overlap1 == 2] = 1
	overlap2[overlap2 == 2] = 0
	num_of_1 = np.sum(overlap2)
	num_of_2 = np.sum(overlap1)
	print (num_of_1,num_of_2)
	ans = (num_of_2 / num_of_1)
	print (num_of_2 / num_of_1)
	return ans
