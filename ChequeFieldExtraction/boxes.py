import cv2
import numpy as np
import utils
import sys
import tesseract_example as tess
import slicing


def isAccountNumber(width, height, x, y, w, h):
	if((x + w < width//2) and (y>height//3 and (y + h)> height//2)):
		return True
	return False

def isDate(width, height, x, y, w, h):
	if(x > width//2 and (y + h) < height//4):
		return True
	return False

def isAmount(width, height, x, y, w, h):
	if((x > width//2) and (y > height//4 and (y + h) < (height - height//4))):
		return True
	return False

def find_boxes(file_name, img_for_box_extraction_path, dir_path, img):
# Read the image
	# path = file_name
	# print(path)
	# img = cv2.imread(path , 0)
	# height, width = img.shape[:2]

	# img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	height, width = img.shape[:2]
	og_img = img
	# Thresholding the image
	(thresh, img_bin) = cv2.threshold(img, 160, 255,cv2.THRESH_BINARY)
	# Invert the image
	img_bin = 255 - img_bin
	#utils.display_image('display_image', img_bin)
	extraction_img = img_bin
	

	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	dilated = cv2.dilate(img_bin, kernel, iterations=2)  # dilate , more the iteration more the dilation
	# utils.display_image('display_image', dilated)
	# utils.store_img(dir_path, "1" + file_name, dilated, "boxes_temp")

	img_bin = dilated

	img_bin = cv2.GaussianBlur(img_bin,(5,5),0)
	# utils.display_image('display_image', img_bin)
	# utils.store_img(dir_path, "2" + file_name, img_bin, "boxes_temp")

	# Defining a kernel length
	kernel_length = np.array(img).shape[1]//80
	 
	# A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
	verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
	# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
	# A kernel of (3 X 3) ones.
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	# Morphological operation to detect vertical lines from an image
	img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=2)
	# utils.display_image('display_image', img_temp1)

	verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=2)
	(thresh, verticle_lines_img) = cv2.threshold(verticle_lines_img, 127, 255,cv2.THRESH_BINARY)
	# utils.display_image('display_image', verticle_lines_img)
	# utils.store_img(dir_path, "3" + file_name, verticle_lines_img, "boxes_temp")


	# Morphological operation to detect horizontal lines from an image
	img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=2)
	# utils.display_image('display_image', img_temp2)

	horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=2)
	(thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 127, 255,cv2.THRESH_BINARY)
	# utils.display_image('display_image', horizontal_lines_img)
	# utils.store_img(dir_path, "4" + file_name, horizontal_lines_img, "boxes_temp")


	# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
	alpha = 0.5
	beta = 1.0 - alpha
	# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
	img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
	# utils.display_image('display_image', img_final_bin)

	img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
	# utils.display_image('display_image', img_final_bin)

	(thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	# utils.display_image('display_image', img_final_bin)
	# utils.store_img(dir_path, "5" + file_name, img_final_bin, "boxes_temp")

	# Find contours for image, which will detect all the boxes
	im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#utils.display_image('display_image', im2)

	# Sort all the contours by top to bottom.
	(contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")

	idx = 0
	account_no_flag = False
	date_flag = False
	amount_flag = False
	account_number_list = []
	amount_list = []
	for c in contours:
	# Returns the location and width,height for every contour
		x, y, w, h = cv2.boundingRect(c)
		if w < width//20 or h < height//20:
			continue
		if (isAccountNumber(width, height, x, y, w, h)):
			account_number_list.append(c)
			# print("Account Number")
			new_img = extraction_img[y:y+h, x:x+w]
		if (isAmount(width, height, x, y, w, h)):
			amount_list.append(c)
			new_img = extraction_img[y:y+h, x:x+w]
		if (isDate(width, height, x, y, w, h) and not date_flag):
			print("Date")
			date_flag = True
			new_img = og_img[y:y+h, x:x+w]
			# new_img = extraction_img[y:y+h, x:x+w]
			# utils.display_image('display_image', new_img)
			utils.store_img(dir_path, file_name, new_img, "date7")

	account_number_list = utils.sort_contours_area(account_number_list)
	amount_list = utils.sort_contours_area(amount_list)
	if len(account_number_list) != 0:
		for i in range(len(account_number_list)):
			x, y, w, h = cv2.boundingRect(account_number_list[0])
			new_img = extraction_img[y:y+h, x:x+w]
			# utils.display_image('display_image', new_img)
			# utils.store_img(dir_path, file_name, new_img, "accNum")
	if len(amount_list) != 0:
		x, y, w, h = cv2.boundingRect(amount_list[0])
		new_img = extraction_img[y:y+h, x:x+w]
		# utils.display_image('display_image', new_img)
		# utils.store_img(dir_path, file_name, new_img, "amount")

	# for c in contours:
	# 	# Returns the location and width,height for every contour
	# 	x, y, w, h = cv2.boundingRect(c)
	# 	if w < width//20 or h < height//20:
	# 		continue
	# 	if (isAccountNumber(width, height, x, y, w, h) and not account_no_flag):
	# 		print("Account Number")
	# 		account_no_flag = True
	# 		new_img = extraction_img[y:y+h, x:x+w]
	# 		# utils.display_image('display_image', new_img)
	# 		utils.store_img(dir_path, file_name, new_img, "accNum")
	# 		# cv2.imwrite(dir_path + "/accNum/" + img_for_box_extraction_path + '.tif', new_img)
	# 		idx = idx+1
	# 		# cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
	# 	if (isAmount(width, height, x, y, w, h) and not amount_flag):
	# 		print("Amount")
	# 		amount_flag = True
	# 		new_img = extraction_img[y:y+h, x:x+w]
	# 		# utils.display_image('display_image', new_img)
	# 		utils.store_img(dir_path, file_name, new_img, "amount")
	# 		# cv2.imwrite(dir_path + "/amount/" + img_for_box_extraction_path + '.tif', new_img)
	# 		idx = idx+1
	# 		# cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
	# 	if (isDate(width, height, x, y, w, h) and not date_flag):
	# 		print("Date")
	# 		date_flag = True
	# 		new_img = extraction_img[y:y+h, x:x+w]
	# 		# utils.display_image('display_image', new_img)
	# 		utils.store_img(dir_path, file_name, new_img, "date")
	# 		# cv2.imwrite(dir_path + "/date/" + img_for_box_extraction_path + '.tif', new_img)
	# 		idx = idx+1

def refine_date(file_name, img_for_box_extraction_path, dir_path, img):
	
	height, width = img.shape[:2]
	img = cv2.resize(img,(width*2, height*2), interpolation = cv2.INTER_LINEAR)
	height, width = img.shape[:2]
	(thresh, img) = cv2.threshold(img, 160, 255,cv2.THRESH_BINARY_INV)
	# utils.display_image('display_image', img)
	og_img = img
	# Invert the image
	img_bin_inv = 255 - img

	# Defining a kernel length
	kernel_length = np.array(img).shape[1]//20
	kernel_length_vertical = height//2
	kernel_length_horizontal = width//4
	# A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
	verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_vertical))
	# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_horizontal, 1))
	# A kernel of (3 X 3) ones.
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
	img_temp = cv2.dilate(img, kernel, iterations=1)
	# utils.display_image('display_image', img_temp)

	# Morphological operation to detect horizontal lines from an image
	img_temp2 = cv2.erode(img_temp, hori_kernel, iterations=1)
	# utils.display_image('display_image', img_temp2)

	horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=1)
	(thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 160, 255,cv2.THRESH_BINARY)
	# utils.display_image('display_image', horizontal_lines_img)


	im2, contours, hierarchy = cv2.findContours(horizontal_lines_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Sort all the contours by top to bottom.
	(contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")

	if len(contours) > 1:
		
		x1, y1, w1, h1 = cv2.boundingRect(contours[0])
		x2, y2, w2, h2 = cv2.boundingRect(contours[len(contours)-1])
		print (cv2.boundingRect(contours[0]))
		print (cv2.boundingRect(contours[len(contours)-1]))
		new_img = img_temp[y1 + h1 : y2, x2 : x1 + w2]
		# utils.display_image('display_image', new_img)
		# utils.store_img(dir_path, file_name, new_img, "date")
		# cv2.imwrite(dir_path + "/date/" + img_for_box_extraction_path + '.tif', new_img)
		# (thresh, new_img) = cv2.threshold(new_img, 32, 255,cv2.THRESH_BINARY)
		# utils.display_image('display_image', new_img)
		final_img = new_img
		# utils.display_image('display_image', final_img)
		# (thresh, final_img) = cv2.threshold(final_img, 32, 255,cv2.THRESH_BINARY)
		# utils.display_image('display_image', final_img)
		#final_image = remove_lines(final_img)
		# utils.store_img(dir_path, file_name, final_img, "date8")
		utils.store_img(dir_path, file_name, final_img, "date9")
		img_temp = final_img

	
	# # Morphological operation to detect horizontal lines from an image
	# img_temp2 = cv2.erode(img_temp, hori_kernel, iterations=1)
	# # utils.display_image('display_image', img_temp2)

	# horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=1)
	# (thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 160, 255,cv2.THRESH_BINARY)
	# # utils.display_image('display_image', horizontal_lines_img)


	# # Morphological operation to detect vertical lines from an image
	# img_temp1 = cv2.erode(img_temp, verticle_kernel, iterations=1)
	# # utils.display_image('display_image', img_temp1)

	# verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=1)
	# (thresh, verticle_lines_img) = cv2.threshold(verticle_lines_img, 160, 255,cv2.THRESH_BINARY)
	# # utils.display_image('display_image', verticle_lines_img)

	# # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
	# alpha = 0.5
	# beta = 1.0 - alpha
	# # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
	# img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
	# # utils.display_image('display_image', img_final_bin)
	# # edges = cv2.Canny(horizontal_lines_img, 127, 255)
	# # lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30,  minLineLength = width//3)
	 
	# # img_bin_inv_contours = img_bin_inv
	# # hori_line_1 = []
	# # hori_line_1 = []
	# # hori_line_2 = []
	# # hori_line_2 = []
	# # if lines is None:
	# # 	return
	# # for line in lines:
	# # 	x1, y1, x2, y2 = line[0]
	# # 	cv2.line(og_img, (x1, y1), (x2, y2), (255, 255, 255), 3)
	# # # utils.display_image('display_image', og_img)
	# # x1, y1, x2, y2 = lines[0][0]
	# # hori_line_1 = [x1, y1]
	# # x1, y1, x2, y2 = lines[0][0]
	# # hori_line_2 = [x1, y1]
	# # image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	# # utils.display_image('display_image', image)

	# # Find contours for image, which will detect all the boxes
	# im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# # Sort all the contours by top to bottom.
	# (contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")

	# idx = 0
	# if len(contours) > 0:
	# 	print ("date")
	# for c in contours:
	# 	# Returns the location and width,height for every contour
	# 	x, y, w, h = cv2.boundingRect(c)
	# 	if w < width//2 or h < height//3:
	# 		continue

	# 	new_img = img_final_bin[y:y+h, x:x+w]
	# 	# utils.display_image('display_image', new_img)
	# 	# utils.store_img(dir_path, file_name, new_img, "date")
	# 	# cv2.imwrite(dir_path + "/date/" + img_for_box_extraction_path + '.tif', new_img)
	# 	# (thresh, new_img) = cv2.threshold(new_img, 32, 255,cv2.THRESH_BINARY)
	# 	# utils.display_image('display_image', new_img)
	# 	final_img = og_img[y:y+h, x:x+w] - new_img
	# 	# utils.display_image('display_image', final_img)
	# 	(thresh, final_img) = cv2.threshold(final_img, 32, 255,cv2.THRESH_BINARY)
	# 	# utils.display_image('display_image', final_img)
	# 	idx = idx+1
	# 	#final_image = remove_lines(final_img)
	# 	# utils.store_img(dir_path, file_name, final_img, "date8")
	# 	break

def refine_accNum(file_name, img_for_box_extraction_path, dir_path, img):
	og_img = img
	height, width = img.shape[:2]
	(thresh, img) = cv2.threshold(img, 160, 255,cv2.THRESH_BINARY)
	# Invert the image
	img_bin_inv = 255 - img

	# Defining a kernel length
	kernel_length = np.array(img).shape[1]//20
	kernel_length_vertical = height//2
	kernel_length_horizontal = width//4
	# A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
	verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_vertical))
	# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_horizontal, 1))
	# A kernel of (3 X 3) ones.
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	# Morphological operation to detect vertical lines from an image
	img_temp1 = cv2.erode(img, verticle_kernel, iterations=1)
	# utils.display_image('display_image', img_temp1)

	verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=1)
	(thresh, verticle_lines_img) = cv2.threshold(verticle_lines_img, 32, 255,cv2.THRESH_BINARY)
	# utils.display_image('display_image', verticle_lines_img)
	

	# Morphological operation to detect horizontal lines from an image
	img_temp2 = cv2.erode(img, hori_kernel, iterations=1)
	# utils.display_image('display_image', img_temp2)

	horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=1)
	(thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 32, 255,cv2.THRESH_BINARY)
	# utils.display_image('display_image', horizontal_lines_img)

	# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
	alpha = 0.5
	beta = 1.0 - alpha
	# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
	img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
	# utils.display_image('display_image', img_final_bin)

	# Find contours for image, which will detect all the boxes
	im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Sort all the contours by top to bottom.
	if(len(contours) != 0):
		(contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")

		idx = 0
		for c in contours:
			# Returns the location and width,height for every contour
			x, y, w, h = cv2.boundingRect(c)
			if w < width//5 or h < height//5:
				continue
			
			new_img = img_final_bin[y:y+h, x:x+w]
			# utils.display_image('display_image', new_img)
			# utils.store_img(dir_path, file_name, new_img, "date")
			# cv2.imwrite(dir_path + "/date/" + img_for_box_extraction_path + '.tif', new_img)
			# (thresh, new_img) = cv2.threshold(new_img, 32, 255,cv2.THRESH_BINARY)
			
			# utils.display_image('display_image', new_img)
			final_img = og_img[y:y+h, x:x+w] - new_img
			# utils.display_image('display_image', final_img)
			(thresh, final_img) = cv2.threshold(final_img, 32, 255,cv2.THRESH_BINARY)
			# utils.display_image('display_image', final_img)
			idx = idx+1
			print (file_name)
			# tess.test(file_name, img)
			# utils.store_img(dir_path, file_name, img, "refined_acc")
			utils.display_image('display_image', final_img)
			# remove_lines(final_img)
			# if idx == 2:
			break

def remove_lines(img):

	height, width = img.shape[:2]
	kernel_length_vertical = height//2
	kernel_length_horizontal = width//10

	verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_vertical))
	# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_horizontal, 1))
	# A kernel of (3 X 3) ones.
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	# Morphological operation to detect vertical lines from an image
	img_temp1 = cv2.erode(img, verticle_kernel, iterations=1)
	# utils.display_image('display_image', img_temp1)

	verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=1)
	(thresh, verticle_lines_img) = cv2.threshold(verticle_lines_img, 0, 255,cv2.THRESH_BINARY)
	# utils.display_image('display_image', verticle_lines_img)
	

	# Morphological operation to detect horizontal lines from an image
	img_temp2 = cv2.erode(img, hori_kernel, iterations=1)
	# utils.display_image('display_image', img_temp2)

	horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=1)
	(thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 0, 255,cv2.THRESH_BINARY)
	# utils.display_image('display_image', horizontal_lines_img)
	
	# utils.display_image('display_image', img)

	# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 1))
	# verticle_lines_img = cv2.dilate(verticle_lines_img, kernel, iterations=1)
	# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 3))
	# horizontal_lines_img = cv2.dilate(horizontal_lines_img, kernel, iterations=1)

	img_remove_vertical = img - verticle_lines_img
	# utils.display_image('display_image', img_remove_vertical)
	img_remove_horizontal = img_remove_vertical - horizontal_lines_img
	#utils.display_image('display_image', img_remove_horizontal)
	return img_remove_horizontal

if __name__ == "__main__":
	import utils
	import sys
	import cv2
	import os
	import glob

	my_path = "./../IDRBT Cheque Image Dataset/300/"
	# filepath = "./samples/"+ str(sys.argv[1])

	store = "./temp1/"

	# onlyfiles = glob.glob(my_path + "*.tif")#Cheque 309133.tif
	# print(onlyfiles)
	# print(len(onlyfiles))
	# i=0
	# for filepath in onlyfiles:
	# 	img = cv2.imread(filepath , 0)
	# 	height, width = img.shape[:2]
	# 	# img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	# 	__, filename = os.path.split(filepath)
	# 	find_boxes(filename, filepath, store, img)
	# 	i+=1

	
	onlyfiles = glob.glob(store + "date7/" + "*.tif")#Cheque 309133.tif 309119 309124 309112
	# onlyfiles = glob.glob(store + "accNum/" + "*.tif")#Cheque 309133.tif 309119 309124 309112
	print(onlyfiles)
	i=0
	for filepath in onlyfiles:
		img = cv2.imread(filepath , 0)
		height, width = img.shape[:2]
		# img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
		__, filename = os.path.split(filepath)
		i+=1
		# print (filename)
		refine_date(filename, filepath, store, img)
		# refine_accNum(filename, store + "accNum/", store, img)
