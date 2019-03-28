
# coding: utf-8

# In[1]:


import cv2
import numpy as np
# import matplotlib.pyplot as plt
import glob
import utils
import os

# In[2]:


def merge_rectangle(list_all_rect,threshold = 2):
	
	#print(list_all_rect)  
	merged_list = []
	start_point = []
	end_point = []
	final_list = []
	for i in range(len(list_all_rect)):
		list_curr = list_all_rect[i]
	
		if i == len(list_all_rect)-1:
			if start_point:
				merged_list.append(start_point+end_point)
			else:
				merged_list.append(list_all_rect[i])
			continue
	
		list_next = list_all_rect[i+1]

		diff = list_next[0] - list_curr[2]
	
		if diff <= threshold and not start_point:
			start_point = [list_curr[0],min(list_curr[1],list_next[1]),i]
			end_point   = [list_next[2],max(list_curr[3],list_next[3]),i+1]
	
		elif diff <= threshold:
			end_point   = [list_next[2],max(list_next[3],end_point[1]),i+1]
	
		else:
			if start_point:
				merged_list.append(start_point+end_point)
			else:
				merged_list.append(list_curr)
			start_point = []
			end_point   = []
  
	return merged_list


# In[3]:


def optimize_merge_rectangle( list_all_rect , max_threshold_to_try = 5 , min_width = 50 , max_width = 250):
	
	#Trying directly max_threshold and then removing lengthy components
	
	merged_list = merge_rectangle(list_all_rect , max_threshold_to_try)
	
	# Removing lengthy Components
	# check for width of merged_component
	# we get the merged component if length is greater than 4 ie 6
	
	optimized_list = []
	
	for i in range(len(merged_list)):
		if len(merged_list[i])<6:
			optimized_list.append(merged_list[i])
			continue
		
		
		if abs(merged_list[i][0] - merged_list[i][3]) >= max_width:
			start_index = merged_list[i][2]
			end_index   = merged_list[i][5]
			print("Start_index",start_index,"End_index",end_index)
			for i in range(start_index,end_index+1):
				optimized_list.append(list_all_rect[i])
		else:
			optimized_list.append([merged_list[i][0],merged_list[i][1],merged_list[i][3],merged_list[i][4]])
	
	print(optimized_list)
	
	optimized_list = fix_smallWords(optimized_list , min_width)
	
	
	return optimized_list


# In[4]:


def fix_smallWords(list_of_rect , min_width = 50):
	
	
	up_align  = 10
	dwn_align = 4
	
	# by how much length should be increase if component is small
	# and there is no nearby component to merge
	increase_length_by = 40
	
	list_of_short = []
	length = len(list_of_rect)
	i = 0
	while i < length :
		
		# index less than min_width needs fixing
		
		if abs(list_of_rect[i][0]-list_of_rect[i][2]) <= min_width :
			
			dist_left  = 999999999 
			dist_right = 999999999
			
			print(abs(list_of_rect[i][0]-list_of_rect[i][2]))
			
			if i!=0:
				dist_left  = abs(list_of_rect[i-1][2] - list_of_rect[i][0])
			if i!=len(list_of_rect)-1:
				dist_right = abs(list_of_rect[i][2] - list_of_rect[i+1][0]) 
			
			print("dist_left",dist_left,"dist_right",dist_right)
			# conditions for no nearby component
			if dist_left>55 and dist_right>55:
				list_temp = list_of_rect[i]
				list_temp[2]+=increase_length_by
				list_of_short.append(list_temp)
				
			
			elif dist_left >= 25 and  dist_right >= 60:
				list_temp = list_of_rect[i]
				list_temp[2]+=increase_length_by
				list_of_short.append(list_temp)
				
			#condition for selection betn nearby components
			#if nearby components are present then merge
			
			# In cursive writing
			# If we consider a word then , generally height of first charatere in word is greater than rest of character
			# and the base of rest of the character is either equal to or a bit higher than starting character
			# up_allign  = dist betn 1st char and rest char
			# down_align = dist betn base of rest of the char and starting character 
			
			elif dist_left<dist_right :
				
				if (list_of_rect[i][1]-list_of_rect[i-1][1] > up_align) and (list_of_rect[i-1][3]-list_of_rect[i][3]>dwn_align):
					list_of_short.append(list_of_rect[i])
					print("1 inside continue")
				else: 
					print("1 outside continue")
					list_prev = list_of_rect[i-1]
					list_curr = list_of_rect[i]

					if abs(list_curr[2]-list_prev[0])>=169:
						list_curr[2]+=20
						list_of_short.append(list_curr)
					else:
						list_of_short.pop()
						list_of_short.append([list_prev[0],min(list_prev[1],list_curr[1]),list_curr[2],max(list_prev[3],list_curr[3])])

				
			elif dist_right<dist_left :
				
				if (list_of_rect[i+1][1]-list_of_rect[i][1] > up_align) and (list_of_rect[i][3]-list_of_rect[i+1][3]>dwn_align):
					list_of_short.append(list_of_rect[i])
					print("2 inside continue")
				
				else:
					print("2 outside continue")
					list_next = list_of_rect[i+1]
					list_curr = list_of_rect[i]

					if abs(list_next[2]-list_curr[0])>=169:
						list_curr[0]+=20  
						list_of_short.append(list_curr)
					else:
						list_of_short.append([list_curr[0],min(list_curr[1],list_next[1]),list_next[2],max(list_curr[3],list_next[3])])
						i = i+1

		else:
			list_of_short.append(list_of_rect[i])
		
		i = i+1
			
	return list_of_short          


# In[5]:

def do_segment(image,name) :

	height , width = image.shape[:2]
	# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	gray = image
	ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)


	my_filter = np.array(([[-1],[0.5],[-1]]), np.float32)
	# my_filter = np.ones((5,5),np.float32)/25
	print (my_filter.shape)
	temp = thresh.copy()
	remaining = cv2.filter2D(temp, -1, my_filter)
	# cv2.imshow("thresh",thresh)

	remaining_np = np.asarray(remaining)
	# utils.display_image1(remaining_np)
	remaining_np[remaining_np > 0] = 255
	# cv2.imshow("remaining_np",remaining_np)

	h1, w1 = remaining_np.shape[:2]
	remaining_np[ : 3*(h1//4),:] = 0
	# cv2.imshow("remaining_np_cut",remaining_np)

	final = thresh - remaining_np
	# cv2.imshow("final_image",final)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	store_path = "./temp1/"
	__, filename = os.path.split(name)

	utils.store_img(store_path, filename, final, "removed_underline")

	# kernel = np.ones((5,5), np.uint8)
	# img_dilation = cv2.dilate(final, kernel, iterations=1)

	# # cols = verticalProjection(img_dilation)
	# # hist = create_histogram(cols, img_dilation)
	# # cv2.imshow("final", img_dilation)
	# # utils.display_image1(hist)

	# im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
	
	# display1 = final.copy()
	# list_all_rect = []

	# for i, ctr in enumerate(sorted_ctrs):
	# # Get bounding box
	# 	x, y, w, h = cv2.boundingRect(ctr)
	
	# 	threshold_width = width//5
	# 	threshold_height = height//3
	# 	print("Threshold Width",threshold_width)
	# 	print("Threshold Height",threshold_height)
		
	# 	if w<=threshold_width and h<=threshold_height :
	# 		continue
			
	# 	print(h,w)
	# 	list_single_rect = [x,y,x+w,y + h]
	# 	list_all_rect.append(list_single_rect)
		
	
	# 	cv2.rectangle(display1,(x, y),( x + w, y + h),(90,0,255),2)
	
	
	
	
	# # print("List of all rectanges detected is :",list_all_rect)
	
	# cv2.imshow('marked area',display1)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	
	# #for k in range(6) :
	# merged_list = []
	# merged_list = optimize_merge_rectangle(list_all_rect,5)
	# print("Merged List is at threshold  :" + str(5) ,merged_list)
	# for j in merged_list:
	# 	widthi = abs(j[0]-j[2])
	# 	print("width",widthi)
	# display2 = final.copy()
	# for i in merged_list:

	#   #crop_img = display2[i[1]:i[3],i[0]:i[2]]
	#   #cv2.imshow('crop',crop_img)
	#   #cv2.waitKey(0)
	#   #cv2.destroyAllWindows()

	# 	cv2.rectangle(display2,(i[0],i[1]),(i[2], i[3]),(90,0,255),2)

	
		
	# cv2.imshow('merged areas at threshold'+str(5)+str(name),display2)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()


# In[ ]:

if __name__ == "__main__":

	directory_path = "./temp1/legal_amount1/"
	images = glob.glob(directory_path + "*.tif")
	count = 0
	for x in images :
		image = cv2.imread(x, 0)
		do_segment(image,x)
	


