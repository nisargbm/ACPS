import boxes
import micrcode
import signature
from slicing import slice_image, slice_image_get_remaining
import underline
import utils
import sys
import cv2
import os
import numpy as np

def eliminate_symbols(filename, filepath, store, img, ref_image):
	# All the 6 methods for comparison in a list
	methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
				'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

	h1, w1 = img.shape[:2]
	img2 = img.copy()
	img3 = img.copy()
	img = img[:, w1//45 : w1//6]
	img2 = img2[:, w1//45: ]
	# utils.display_image1(img)
	# utils.display_image1(temp_eng)
	
	ref_image = cv2.resize(ref_image,(w1//15, h1//2), interpolation = cv2.INTER_AREA)
	w1 = w1//15	
	h, w = ref_image.shape[:2]
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	img = cv2.dilate(img, kernel, iterations=1)
	# for meth in methods:
	# img = img2.copy()
	method = eval('cv2.TM_CCOEFF_NORMED')
	# Apply template Matching
	res = cv2.matchTemplate(img,ref_image,method)
	# print (res)
	threshold = 0.2
	loc = np.where( res >= threshold)
	# print (loc)
	pts = []
	for i in range(len(loc[0])):
		pts.append([loc[1][i], loc[0][i]])
	# print (pts)
	# pts.sort(key = lambda x: x[0])

	pt = pts[0]
	cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), 255, 2)
	utils.display_image1(img)
	# for pt in pts:
	# 	print (pt)
		# top_left = max_loc
		# bottom_right = (top_left[0] + w, top_left[1] + h)
		# cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2)

		# img2[ :, top_left[0] : bottom_right[0]] = 0
		# utils.display_image1(img)
	# utils.display_image1(img)
	# print (len(loc))
	# if len(loc):
	# 	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	# 	# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
	# 	if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
	# 		top_left = min_loc
	# 	else:
	# 		top_left = max_loc
	# 	bottom_right = (top_left[0] + w, top_left[1] + h)
	# 	cv2.rectangle(img,top_left, bottom_right, 255, 2)
	# 	img2[ :, top_left[0] : bottom_right[0]] = 0
	# 	utils.display_image1(img)
	# 	# utils.store_img(store, filename, img2, "remove_rupees")


if __name__ == "__main__":
	# my_path = "./temp1/handwritten/"
	my_path = "./temp1/legal_amount/"
	my_sample_path = "./samples/"
	template_english_path  = "./samples/rupees_english_template.jpeg"
	template_hindi_path  = "./samples/rupees_hindi_template.jpeg"
	# filepath = "./samples/"+ str(sys.argv[1])
	# filepath = "./temp/acc/"+ str(sys.argv[1])
	# file_path = "./temp/accNum/"

	store = "./temp1/"

	import glob
	onlyfiles = glob.glob(my_path + "underline_3_Cheque *.tif")#Cheque 309159,309069 ,underline_3_Cheque 100834.tif, 083654.tif
	print(onlyfiles)
	i=0
	temp_eng = cv2.imread(template_english_path , 0)
	(thresh, temp_eng) = cv2.threshold(temp_eng, 127, 255,cv2.THRESH_BINARY_INV)
	# utils.display_image1(temp_eng)
	temp_hin = cv2.imread(template_hindi_path , 0)
	(thresh, temp_hin) = cv2.threshold(temp_hin, 127, 255,cv2.THRESH_BINARY_INV)
	for filepath in onlyfiles:
		img = cv2.imread(filepath , 0)
		height, width = img.shape[:2]
		__, filename = os.path.split(filepath)
		# utils.display_image1(img)
		eliminate_symbols(filename, filepath, store, img, temp_eng)
		# eliminate_symbols(filename, filepath, store, img, temp_hin)
		i+=1


# if __name__ == "__main__":
# 	my_path = "./../IDRBT Cheque Image Dataset/300/"
# 	my_sample_path = "./samples/"
# 	# filepath = "./samples/"+ str(sys.argv[1])
# 	# filepath = "./temp/acc/"+ str(sys.argv[1])
# 	# file_path = "./temp/accNum/"

# 	store = "./temp1/"

# 	import glob
# 	onlyfiles = glob.glob(my_path + "Cheque 3" + "*.tif")
# 	print(onlyfiles)
# 	i=0
# 	for filepath in onlyfiles:
# 		img = cv2.imread(filepath , 0)

# 		img = cv2.resize(img,(2000, 750), interpolation = cv2.INTER_AREA)
# 		height, width = img.shape[:2]
# 		x_min = width//11
# 		y_min = 3 * (height//10)

# 		x_max = width - width//5
# 		y_max = y_min + height//10

# 		# h = y_min + height//7
# 		# w = width - x_max
# 		__, filename = os.path.split(filepath)
# 		# underline.get_underline(filename, filepath, store, img)
# 		crop = img[y_min : y_max, x_min : x_max]
# 		utils.display_image1(crop)
# 		cv2.imwrite("./temp1/abcd/" + filename, crop)
# 		i+=1