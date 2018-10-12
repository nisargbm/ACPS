import cv2
import numpy as np
import utils
import random
import sys

dir_path = "./temp/"
img_for_box_extraction_path = str(sys.argv[1]) ##Provide argument as sample/Cheque.tif

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

img_bin_inv_blur = cv2.GaussianBlur(img_bin_inv,(3,3),0)
utils.display_image('display_image', img_bin_inv_blur)

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,2))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
img_bin_inv_blur_dilated = cv2.dilate(img_bin_inv_blur, kernel, iterations=3)  # dilate , more the iteration more the dilation
utils.display_image('display_image', img_bin_inv_blur_dilated)

kernel_length = np.array(img_bin).shape[1]//10
hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

img_temp_horizontal = cv2.erode(img_bin_inv_blur_dilated, hori_kernel, iterations=1)
utils.display_image('display_image', img_temp_horizontal)

horizontal_lines_img = cv2.dilate(img_temp_horizontal, hori_kernel, iterations=2)
utils.display_image('display_image', horizontal_lines_img)

edges = cv2.Canny(horizontal_lines_img, 75, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)
 
img_bin_inv_contours = img_bin_inv

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img_bin_inv, (x1, y1), (x2, y2), (0, 255, 0), 3)
 
utils.display_image("Edges", edges)
utils.display_image("Image", img_bin_inv)

image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
utils.display_image('display_image', image)

cv2.drawContours(img_bin_inv_contours, contours, -1, (0,255,0), 3)
utils.display_image('display_image', img_bin_inv_contours)

# Sort all the contours by top to bottom.
(contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")

for contour in contours:
    # get rectangle bounding contour
    [x, y, w, h] = cv2.boundingRect(contour)

    # Don't plot small false positives that aren't text
    if w < width/(2.5):
        continue

    # draw rectangle around contour on original image
    cv2.rectangle(og_image_contours, (x, y - (height//8)), (x + w, y + h), (0, 0, 0), 2)
    if((y - ( height / 8)) >= 0):
        crop_img = og_img[y - (height//10) : y + h + (height // 100), x : x + w]
        utils.display_image('captcha_result', crop_img)
        #cv2.imwrite( "./temp/" + str(random.randint(0,10000)) + ".jpg", crop_img);
    '''
    #you can crop image and send to OCR  , false detected will return no text :)
    cropped = img_final[y :y +  h , x : x + w]

    s = file_name + '/crop_' + str(index) + '.jpg' 
    cv2.imwrite(s , cropped)
    index = index + 1

    '''
# write original image with added contours to disk
cv2.imshow('display_image', og_image_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()






