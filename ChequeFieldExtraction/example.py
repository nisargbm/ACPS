import utils
import sys
import cv2
import os
import numpy as np

my_path = "./temp1/legal_amount1/"
my_sample_path = "./output/"
# filepath = "./samples/"+ str(sys.argv[1])
# filepath = "./temp/acc/"+ str(sys.argv[1])
# file_path = "./temp/accNum/"

store = "./temp1/"

def convertit(img):
	# utils.display_image1(img)
	utils.display_image1(img)
	(thresh, img) = cv2.threshold(img, 32, 255, cv2.THRESH_BINARY_INV)
	utils.display_image1(img)
	og_img = img.copy()
	height, width = img.shape[:2]
	for i in range(width):
		counti = np.count_nonzero(img[:,i])
		if counti<2:
			img[:,i] = 0
	front = 0
	back = 0
	list_valid = []
	within_text = False
	add = False
	
	for i in range(width):
		counti = np.count_nonzero(img[:,i])
		if counti > 0:
			if not within_text:
				front = i
				back = front + 1
				within_text = True
			else:
				back = back + 1
		else:
			if not within_text:
				continue
			else:
				within_text = False
				list_valid.append([front, back])

	if within_text:
		back = width
		list_valid.append([front, back])

	print (list_valid)
	# for x in list_valid:
	# 	og_img[:, x[0]:x[1]] = 255
	# utils.display_image1(og_img)
	image = np.zeros((height, 1), np.uint8)
	gap = np.zeros((height, 1), np.uint8)
	for coor in list_valid:
		h1, w1 = image.shape[:2]
		h2, w2 = gap.shape[:2]
		wide = coor[1] - coor[0]
		vis = np.zeros((height, w1 + w2 + wide), np.uint8)
		vis[:, :w1] = image
		vis[:, w1 : w1 + w2] = gap
		vis[:, w1 + w2 : w1 + w2 + wide] = img[:, coor[0]:coor[1]]
		image = vis
	utils.display_image1(image)
	image = cv2.resize(image,(100, 30), interpolation = cv2.INTER_LINEAR)
	return image

			# vis = np.zeros((height, w1+w2), np.uint8)
			# crop_img = output_image
			# h1, w1 = amount_image.shape[:2]
			# h2, w2 = crop_img.shape[:2]
			# vis = np.zeros((height, w1+w2), np.uint8)
			# vis[:h1, :w1] = amount_image
			# vis[:h2, w1:w1+w2] = crop_img
			# amount_image = vis

def deskew(img):
    m = cv2.moments(img)
    height, width = img.shape[:2]
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*width*skew], [0, 1, 0]])
    img = cv2.warpAffine(img, M, (width, height), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR, borderValue=(255,255,255))
    return img

import glob
onlyfiles = glob.glob(my_sample_path + "*.png")
print(onlyfiles)
i=0
for filepath in onlyfiles:
	img = cv2.imread(filepath , 0)
	img = cv2.resize(img,(100, 30), interpolation = cv2.INTER_AREA)
	(thresh, temp) = cv2.threshold(img, 32, 255, cv2.THRESH_BINARY_INV)
	# element = cv2.getStructuringElement(cv2.MORPH_RECT,(2,1))
	# eroded = cv2.erode(temp, element, iterations = 1)
	(thresh, eroded) = cv2.threshold(temp, 32, 255, cv2.THRESH_BINARY_INV)
	# img = convertit(eroded)
	utils.display_image1(eroded)
	img = deskew(eroded)
	# __, filename = os.path.split(filepath)
	utils.display_image1(img)
	# utils.store_img(store, filename, img, "legal_amount")
	i+=1

