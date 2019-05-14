import cv2
import numpy as np
import utils
import random
import sys
import slicing

# dir_path = "./temp/"
# img_for_box_extraction_path = str(sys.argv[1]) ##Provide argument as sample/Cheque.tif


# Read the image
#og_img = cv2.imread(img_for_box_extraction_path, 0)
# def get_underline(img_for_extraction_path, file_name, dir_path, img):
# 	# height, width = og_img.shape[:2]

# 	# og_img = cv2.resize(og_img,(width//2, height//2), interpolation = cv2.INTER_AREA)
# 	height, width = img.shape[:2]
# 	og_img = slicing.slice_image_get_remaining(img)
# 	og_image_contours = og_img

# 	#utils.display_image('display_image', og_img)

# 	# Thresholding the image
# 	(thresh, img_bin) = cv2.threshold(og_img, 160, 255,cv2.THRESH_BINARY)
# 	# Invert the image
# 	#utils.display_image('display_image', img_bin)

# 	img_bin_inv = 255-img_bin
# 	img_bin_inv_final = 255-img_bin
# 	#utils.display_image('display_image', img_bin_inv)

# 	img_bin_inv_blur = cv2.GaussianBlur(img_bin_inv,(3,3),0)
# 	# utils.display_image('display_image', img_bin_inv_blur)

# 	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,2))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
# 	img_bin_inv_blur_dilated = cv2.dilate(img_bin_inv_blur, kernel, iterations=3)  # dilate , more the iteration more the dilation
# 	utils.display_image('display_image', img_bin_inv_blur_dilated)

# 	kernel_length = np.array(img_bin).shape[1]//5
# 	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

# 	img_temp_horizontal = cv2.erode(img_bin_inv_blur_dilated, hori_kernel, iterations=1)
# 	# utils.display_image('display_image', img_temp_horizontal)

# 	horizontal_lines_img = cv2.dilate(img_temp_horizontal, hori_kernel, iterations=1)
# 	# utils.display_image('display_image', horizontal_lines_img)
# 	# utils.store_img(dir_path, img_for_extraction_path, horizontal_lines_img, "handwritten")

# 	(thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 32, 255,cv2.THRESH_BINARY)
# 	#utils.display_image('display_image', horizontal_lines_img)
# 	horizontal_lines_img = cv2.GaussianBlur(horizontal_lines_img,(5,5),0)
# 	#utils.display_image('display_image', horizontal_lines_img)

# 	edges = cv2.Canny(horizontal_lines_img, 127, 255)
# 	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30,  minLineLength = height//1.5)
	 
# 	img_bin_inv_contours = img_bin_inv

# 	# if lines is None:
# 	# 	return
# 	# for line in lines:
# 	# 	x1, y1, x2, y2 = line[0]
# 	# 	cv2.line(img_bin_inv_contours, (x1, y1), (x2, y2), (0, 255, 0), 3)

# 	image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
# 	#utils.display_image('display_image', image)

# 	cv2.drawContours(img_bin_inv_contours, contours, -1, (255,255,255), 3)
# 	utils.display_image('display_image', img_bin_inv_contours)

# 	# Sort all the contours by top to bottom.
# 	(contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")
# 	idx = 0
# 	underline = "underline"
# 	for contour in contours:
# 		# get rectangle bounding contour
# 		[x, y, w, h] = cv2.boundingRect(contour)

# 		# Don't plot small false positives that aren't text
# 		if w < width/(2):
# 			continue

# 		# draw rectangle around contour on original image
# 		# cv2.rectangle(og_image_contours, (x, y , (x + w, y + h + (height // 100), (0, 0, 0), 2)
# 		if ((y - ( height // 8)) > 0) :
# 			crop_img = img_bin_inv_final[y - (height // 12) : y + h + (height // 100),  : ]
# 			utils.display_image('captcha_result', crop_img)
# 			# print("Underline")
# 			# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, crop_img, "handwritten")
# 		else:
# 			# crop_img = img_bin_inv_final[0 : y + h + (height // 100), x : x + w]
# 			crop_img = img_bin_inv_final[0 : y + h + (height // 100), :]
# 			utils.display_image('captcha_result', crop_img)
# 			# print("Underline")
# 			# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, crop_img, "handwritten")
# 		idx = idx + 1

def get_underline(img_for_extraction_path, file_name, dir_path, img):
	# height, width = og_img.shape[:2]

	# og_img = cv2.resize(og_img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	height, width = img.shape[:2]
	og_img = slicing.slice_image_get_remaining(img)
	og_image_contours = og_img

	utils.display_image('display_image', og_img)

	# Thresholding the image
	(thresh, img_bin) = cv2.threshold(og_img, 160, 255,cv2.THRESH_BINARY)
	# Invert the image
	utils.display_image('display_image', img_bin)

	img_bin_inv = 255-img_bin
	img_bin_inv_final = 255-img_bin
	utils.display_image('display_image', img_bin_inv)
	# utils.store_img(dir_path, str(1) + "_" + img_for_extraction_path, img_bin_inv, "images_for_paper")

	img_bin_inv_blur = cv2.GaussianBlur(img_bin_inv,(3,3),0)
	utils.display_image('display_image', img_bin_inv_blur)

	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,2))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	img_bin_inv_blur_dilated = cv2.dilate(img_bin_inv_blur, kernel, iterations=3)  # dilate , more the iteration more the dilation
	utils.display_image('display_image', img_bin_inv_blur_dilated)

	# utils.store_img(dir_path, str(2) + "_" + img_for_extraction_path, img_bin_inv_blur_dilated, "images_for_paper")

	kernel_length = np.array(img_bin).shape[1]//5
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

	img_temp_horizontal = cv2.erode(img_bin_inv_blur_dilated, hori_kernel, iterations=1)
	utils.display_image('display_image', img_temp_horizontal)

	# utils.store_img(dir_path, str(3) + "_" + img_for_extraction_path, img_temp_horizontal, "images_for_paper")

	horizontal_lines_img = cv2.dilate(img_temp_horizontal, hori_kernel, iterations=1)
	utils.display_image('display_image', horizontal_lines_img)
	# utils.store_img(dir_path, img_for_extraction_path, horizontal_lines_img, "handwritten")

	(thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 32, 255,cv2.THRESH_BINARY)
	utils.display_image('display_image', horizontal_lines_img)
	utils.store_img(dir_path, str("3a") + "_" + img_for_extraction_path, horizontal_lines_img, "images_for_paper")

	horizontal_lines_img = cv2.GaussianBlur(horizontal_lines_img,(5,5),0)
	utils.display_image('display_image', horizontal_lines_img)

	edges = cv2.Canny(horizontal_lines_img, 127, 255)
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30,  minLineLength = height//1.5)

	 
	img_bin_inv_contours = img_bin_inv

	# if lines is None:
	# 	return
	# for line in lines:
	# 	x1, y1, x2, y2 = line[0]
	# 	cv2.line(img_bin_inv_contours, (x1, y1), (x2, y2), (0, 255, 0), 3)

	image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	utils.display_image('display_image', image)

	# utils.store_img(dir_path, str(4) + "_" + img_for_extraction_path, image, "images_for_paper")

	cv2.drawContours(img_bin_inv_contours, contours, -1, (255,255,255), 3)
	utils.display_image('display_image', img_bin_inv_contours)

	# Sort all the contours by top to bottom.
	(contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")
	idx = 0
	underline = "underline"
	flag = False
	amount_image = None
	previous = None
	# utils.display_image1(img_bin_inv_final)
	for contour in contours:
		# get rectangle bounding contour
		[x, y, w, h] = cv2.boundingRect(contour)
		# Don't plot small false positives that aren't text
		if w < width/(2):
			continue

		if ((y - ( height // 8)) > 0) :
			utils.display_image('captcha_result', img_bin_inv_final[y - (height // 10) : y + h + (height // 100), width//10 : width - width//5])
			# utils.display_image('captcha_result', crop_img)
			# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, crop_img, "handwritten_payee")
		else:
			# crop_img = img_bin_inv_final[0 : y + h + (height // 100), x : x + w]
			utils.display_image('captcha_result', img_bin_inv_final[0 : y + h + (height // 100), width//10 : width - width//5])

		utils.display_image('captcha_result', img_bin_inv_final[y - (height // 10) : y + h + (height // 100), width//10 : width - width//5])
		# y_act = y - (height // 12)
		# h_act = y_act + (height // 12) + (h + (height // 100))
		if flag:
			if previous is None:
				# print ("Previous is None")
				previous = [0, y, width, h]
			else:
				# print (previous)
				# print ([0, y, width, h])
				overlap = utils.find_overlap(img_bin_inv_final, previous, [0, y, width, h])
				# previous = [0, y, width, h]
				if overlap > 0.1:
					continue
				else:
					previous = [0, y, width, h]
		if not flag:
			# draw rectangle around contour on original image
			# cv2.rectangle(og_image_contours, (x, y , (x + w, y + h + (height // 100), (0, 0, 0), 2)
			flag = True
			# delta = (height // 100)
			if ((y - ( height // 8)) > 0) :
				crop_img = img_bin_inv_final[y - (height // 10) : y + h + (height // 100), width//10 : width - width//5]
				# utils.display_image('captcha_result', crop_img)
				# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, crop_img, "handwritten_payee")
			else:
				# crop_img = img_bin_inv_final[0 : y + h + (height // 100), x : x + w]
				crop_img = img_bin_inv_final[0 : y + h + (height // 100), width//10 : width - width//5]
				# utils.display_image('captcha_result', crop_img)
				# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, crop_img, "handwritten_payee")
		else:
			if ((y - ( height // 8)) > 0) :
				crop_img = img_bin_inv_final[y - (height // 12) : y + h + (height // 100),  : ]
			else:
				# crop_img = img_bin_inv_final[0 : y + h + (height // 100), x : x + w]
				crop_img = img_bin_inv_final[0 : y + h + (height // 100), :]
				# utils.display_image('captcha_result', crop_img)
				# print("Underline")
				# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, crop_img, "handwritten")
			if amount_image is None:
				amount_image = crop_img
			else:		
				h1, w1 = amount_image.shape[:2]
				h2, w2 = crop_img.shape[:2]
				vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
				vis[:h1, :w1] = amount_image
				vis[:h2, w1:w1+w2] = crop_img
				amount_image = vis
			# utils.display_image('captcha_result', amount_image)
			# print("Underline")
			# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, crop_img, "handwritten")
		idx = idx + 1
	height, width = amount_image.shape[:2]
	# utils.display_image('captcha_result', amount_image)
	amount_image[:, width - ((width)//5):] = 0
	# utils.display_image('captcha_result', amount_image)

	# width//2 - (width//2)//20
	amount_image[:,width//2 - (width//2)//15 : width//2 + (width//2)//15] = 0
	# utils.display_image('captcha_result', amount_image)
	# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, amount_image, "handwritten_concatenated")
	if idx == 4:
		print (file_name)

	amount_image = amount_image[:, :width//2]
	# utils.store_img(dir_path, str(5) + "_" + img_for_extraction_path, amount_image, "images_for_paper")
	# utils.store_img(dir_path, underline + "_" + str(idx) + "_" + img_for_extraction_path, amount_image, "handwritten")

def remove_underline_name(img_for_extraction_path, file_name, dir_path, img):

	height, width = img.shape[:2]
	img = img[ height//20 : , width//20 : width - width//5]
	final_img = img
	temp_image = img
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	img_dilated = cv2.dilate(img, kernel, iterations=2)  # dilate , more the iteration more the dilation
	# utils.display_image('display_image', img_dilated)

	kernel_length = np.array(img_dilated).shape[1]//5
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

	img_temp_horizontal = cv2.erode(img_dilated, hori_kernel, iterations=1)
	# utils.display_image('display_image', img_temp_horizontal)

	horizontal_lines_img = cv2.dilate(img_temp_horizontal, hori_kernel, iterations=3)
	# utils.display_image('display_image', horizontal_lines_img)

	new_img = img - horizontal_lines_img
	# utils.display_image('display_image', new_img)
	final_img = new_img

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	dilated_img = cv2.dilate(new_img, kernel, iterations=2)
	# utils.display_image('display_image', dilated_img)
	new_img = dilated_img
	
	im2, contours, hierarchy = cv2.findContours(new_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#utils.display_image('display_image', im2)

	(contours, boundingBoxes) = utils.sort_contours(contours, method="left_to_right")

	# contours = utils.sort_contours_area(contours)
	
	length = len(contours)
	trim_size = length // 5
	print ("Length : " + str(length) + " -- trim_size : " + str(trim_size))
	for i in range(0, length):
# and i < length - 2*trim_size
		if(i >= trim_size):
			continue

		contour = contours[i]
		# get rectangle bounding contour
		[x, y, w, h] = cv2.boundingRect(contour)

		if w > width//50 and h > height//2:
			continue
		# Don't plot small false positives that aren't text
		# if  w < width//50 or h < height//3:
		# 	continue

		# draw rectangle around contour on original image
		cv2.rectangle(temp_image, (x , y), (x + w , y + h), (255, 255, 255), 2)
		crop_img = new_img[y : y + h, x : x + w]
		# utils.display_image('captcha_result', crop_img)
		# new_img[y : y + h, x : x + w] = 0
		final_img[y : y + h, x : x + w] = 0
		# utils.display_image('captcha_result', new_img)
		print("contour")
	# utils.display_image('captcha_result', final_img)
	utils.store_img(dir_path, img_for_extraction_path, final_img, "name")

def remove_underline_amount(img_for_extraction_path, file_name, dir_path, img):
	# utils.store_img(dir_path, img_for_extraction_path, final_img, "amount")

	height, width = img.shape[:2]
	# img = img[ height//20 : , width//20 : width - width//5]
	final_img = img
	temp_image = img
	utils.display_image('display_image', img)

	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	img_dilated = cv2.dilate(img, kernel, iterations=2)  # dilate , more the iteration more the dilation
	utils.display_image('display_image', img_dilated)

	kernel_length = np.array(img_dilated).shape[1]//8
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

	img_temp_horizontal = cv2.erode(img_dilated, hori_kernel, iterations=1)
	utils.display_image('display_image', img_temp_horizontal)

	horizontal_lines_img = cv2.dilate(img_temp_horizontal, hori_kernel, iterations=1)
	utils.display_image('display_image', horizontal_lines_img)

	new_img = img - horizontal_lines_img
	utils.display_image('display_image', new_img)
	# final_img = new_img[height//20 : , width//20 : width]
	final_img = new_img[height//20 : , :]

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	dilated_img = cv2.dilate(new_img, kernel, iterations=2)
	utils.display_image('display_image', dilated_img)
	new_img = dilated_img
	
	# im2, contours, hierarchy = cv2.findContours(new_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# # utils.display_image('display_image', im2)

	# (contours, boundingBoxes) = utils.sort_contours(contours, method="left_to_right")

	# # contours = utils.sort_contours_area(contours)

# 	length = len(contours)
# 	trim_size = length // 2
# 	print ("Length : " + str(length) + " -- trim_size : " + str(trim_size))
# 	for i in range(0, length):
# # and i < length - 2*trim_size
# 		if(i >= trim_size):
# 			continue

# 		contour = contours[i]
# 		# get rectangle bounding contour
# 		[x, y, w, h] = cv2.boundingRect(contour)

# 		if w > width//50 and h > height//2:
# 			continue
# 		# Don't plot small false positives that aren't text
# 		# if  w < width//50 or h < height//3:
# 		# 	continue

# 		# draw rectangle around contour on original image
# 		cv2.rectangle(temp_image, (x , y), (x + w , y + h), (255, 255, 255), 2)
# 		crop_img = new_img[y : y + h, x : x + w]
# 		# utils.display_image('captcha_result', new_img[y : y + h, x : x + w])
# 		# new_img[y : y + h, x : x + w] = 0
# 		final_img[y : y + h, x : x + w] = 0
# 		# utils.display_image('captcha_result', final_img)
# 		print("contour")

	# utils.display_image('captcha_result', final_img)
	# utils.store_img(dir_path, img_for_extraction_path, final_img, "name")
	utils.store_img(dir_path, str(6) + "_" + img_for_extraction_path, final_img, "images_for_paper")



if __name__ == "__main__":
	import utils
	import sys
	import cv2
	import os

	my_path = "./../IDRBT Cheque Image Dataset/300/"
	# filepath = "./samples/"+ str(sys.argv[1])

	store = "./temp/"

	import glob
	onlyfiles = glob.glob(my_path + "Cheque *.tif")#Cheque 309159,309069
	print(onlyfiles)
	i=0
	for filepath in onlyfiles:
		img = cv2.imread(filepath , 0)
		height, width = img.shape[:2]
		img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
		__, filename = os.path.split(filepath)
		get_underline(filename, filepath, store, img)
		i+=1

	# onlyfiles = glob.glob(store + "images_for_paper/" + "5_Cheque 309159.tif")
	# # onlyfiles = glob.glob(store + "handwritten/" + "*.tif")
	# print(onlyfiles)
	# i=0
	# for filepath in onlyfiles:
	# 	img = cv2.imread(filepath , 0)
	# 	height, width = img.shape[:2]
	# 	# img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
	# 	__, filename = os.path.split(filepath)
	# 	i+=1

	# 	# remove_underline_name(filename, filepath, store, img)
	# 	remove_underline_amount(filename, filepath, store, img)

