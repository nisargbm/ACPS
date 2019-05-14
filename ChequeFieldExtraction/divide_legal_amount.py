from skimage.segmentation import clear_border
from imutils import contours
import imutils
import numpy as np
import argparse
import imutils
import cv2
import sys
import os


# def divide(img):

	# img = cv2.bilateralFilter(img, 11, 17, 17)
	# utils.display_image('display_image', img)
	# edged = cv2.Canny(img, 30, 200)
	# utils.display_image('display_image', edged)
	# im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	# #utils.display_image('display_image', im2)

	# # Sort all the contours by top to bottom.
	# # (contours, boundingBoxes) = utils.sort_contours(contours, method="left-to-right")
	# contours = utils.sort_contours_area(contours)

	# for c in contours:
	# 	x, y, w, h = cv2.boundingRect(c)
	# 	cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
	# 	utils.display_image('display_image', img)
	# Find the contours
	# image,contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	# For each contour, find the bounding rectangle and draw it
	# for cnt in contours:
	#     x,y,w,h = cv2.boundingRect(cnt)
	#     cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	#     utils.display_image('display_image', img)

def verticalProjection(img):
	"Return a list containing the sum of the pixels in each column"
	(h, w) = img.shape[:2]
	# ones = np.zeros(img.shape,np.uint8)
	# ones[ones > 0] = 1
	# img = ones
	sumCols = []
	for j in range(w):
		col = img[0:h, j:j+1] # y1:y2, x1:x2
		sumCols.append(np.count_nonzero(col))
	return sumCols

def create_histogram(sumCols, img):
	h, w = img.shape[:2]
	hist = np.zeros(img.shape,np.uint8)
	hist = 255 - hist
	for i in range(len(sumCols)):
		hist[:sumCols[i],i] = 0
	return hist

def threshold_mean(img, sumCols): 
	values = []
	for val in sumCols:
		if val != 0:
			values.append(val)
	values = sumCols
	# mean = np.mean(values)
	mean = np.median(values)

	for i in range(len(sumCols)):
		if sumCols[i] < mean:
			sumCols[i] = 0

	# hist = create_image(sumCols, img)
	# cv2.imshow('display', img)
	# utils.display_image('display_image', hist)
	return sumCols

def my_dilate(img, sumCols):
	output_cols = []
	output_cols.append(sumCols[0])
	for i in range(1,len(sumCols)-1):
		temp = int((sumCols[i-1] + sumCols[i] + sumCols[i+1])/3)
		output_cols.append(temp)
	output_cols.append(output_cols[len(output_cols)-1])

	# hist = create_image(sumCols, img)
	# hist1 = create_image(output_cols, img)

	# cv2.imshow('image', img)
	# cv2.imshow('og_hist', hist)
	# utils.display_image('new_hist', hist1)

	return output_cols

def calculate(img, sumCols):
	for i in range(len(sumCols)):
		if sumCols[i] is 0:
			img[:, i] = 255
	utils.display_image('display_image', img)	

def skeletonize(img):
	size = np.size(img)
	skel = np.zeros(img.shape,np.uint8)
	height, width = img.shape[:2]

	ret,img = cv2.threshold(img,127,255,0)
	element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	done = False
	 
	while( not done):
		eroded = cv2.erode(img,element)
		temp = cv2.dilate(eroded,element)
		temp = cv2.subtract(img,temp)
		skel = cv2.bitwise_or(skel,temp)
		img = eroded.copy()
	 
		zeros = size - cv2.countNonZero(img)
		if zeros==size:
			done = True

	# utils.display_image('display_image', skel)
	return skel

def upward(img):
	(thresh,img) = cv2.threshold(img,127,255,0)
	# img = 255 - img
	# utils.display_image('display_image', img)

	height, width = img.shape[:2]
	cols = [0] * width
	for i in range(width):
		for j in range(height - 1, -1, -1):
			print ("hi")
			if img[j,i] == 255:
				cols[i] = j
				break

	print (cols)
	# h, w = img.shape[:2]
	# hist = np.zeros(img.shape,np.uint8)
	# # hist = 255 - hist
	# for i in range(len(cols)):
	# 	hist[cols[i]:,i] = 255

	# hist = 255 - hist
	# cv2.imshow('og_image', img)
	# utils.display_image('display_image', hist)
	return cols

def downward(img, upward_cols):
	(thresh,img) = cv2.threshold(img,127,255,0)
	# img = 255 - img
	# utils.display_image('display_image', img)

	height, width = img.shape[:2]
	downward_cols = [0] * width
	for i in range(width):
		for j in range(0, height):
			print ("hi")
			if img[j,i] == 255:
				downward_cols[i] = j
				break

	print (downward_cols)
	h, w = img.shape[:2]
	hist = np.zeros(img.shape,np.uint8)
	# hist = 255 - hist
	for i in range(len(downward_cols)):
		hist[downward_cols[i] : upward_cols[i],i] = 255

	
	cols = verticalProjection(hist)
	# cols = my_dilate(img, cols)
	hist = create_histogram(cols, img)
	hist = 255 - hist
	cv2.imshow('og_image', img)
	utils.display_image('display_image', hist)

	return downward_cols

if __name__ == "__main__":

	import utils
	import sys
	import cv2
	import os

	my_path = "./temp/legal_amount/"
	my_path_amount = "./temp/amount/"
	# filepath = "./samples/"+ str(sys.argv[1])

	store = "./temp1/"

	import glob
	onlyfiles = glob.glob(my_path + "*.tif")#Cheque 309159,309069 ,underline_3_Cheque 100834.tif, 083654.tif
	print(onlyfiles)
	i=0
	for filepath in onlyfiles:
		img = cv2.imread(filepath , 0)
		height, width = img.shape[:2]
		img1 = img.copy()
		# img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
		# img = img[:, width//35 :]
		# utils.display_image('display_image', img)
		__, filename = os.path.split(filepath)
		# divide(img)
		# img = skeletonize(img)
		# upward_cols = upward(img)
		# downward_cols = downward(img, upward_cols)

		# utils.display_image('display_image', img)
		# # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
		# # img = cv2.dilate(img, kernel, iterations=1)
		# # img = cv2.erode(img, kernel, iterations=1)
		cols = verticalProjection(img)
		hist = create_histogram(cols, img)
		cv2.imshow('og_image', img)
		utils.display_image('display_image', hist)
		# cols = threshold_mean(img, cols)
		# output_cols = my_dilate(img,cols)
		# calculate(img1, output_cols)
		# utils.store_img(store, filename, img, "legal_amount1")
		i+=1