import numpy as np
import cv2

# img = cv2.imread('Cheque.tif')
# # cv2.imshow('image', img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# # cv2.imshow('color_image',img)
# # cv2.imshow('gray_image',imgray) 
# # cv2.waitKey(0)                 # Waits forever for user to press any key
# # cv2.destroyAllWindows()

# ret,thresh = cv2.threshold(imgray,200,255,0)

# _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours, -1, (0,255,0), 3)

# cv2.imshow('color_image',img)
# # cv2.imshow('gray_image',imgray) 
# cv2.waitKey(0)                 # Waits forever for user to press any key
# cv2.destroyAllWindows()


file_name = 'Cheque.tif'
img = cv2.imread(file_name)

img_final = cv2.imread(file_name)
img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('captcha_resul', new_img)
cv2.waitKey()
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2)) 
erosion = cv2.erode(new_img,kernel,iterations = 2)
cv2.imshow('captcha_resul', erosion)
cv2.waitKey()
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
dilated = cv2.dilate(erosion, kernel, iterations=5)  # dilate , more the iteration more the dilation
cv2.imshow('captcha_resul', dilated)
cv2.waitKey()
image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('captcha_resul', img)
cv2.waitKey()
for contour in contours:
    # get rectangle bounding contour
    [x, y, w, h] = cv2.boundingRect(contour)

    # Don't plot small false positives that aren't text
    if w < 35 and h < 35:
        continue

    # draw rectangle around contour on original image
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

    '''
    #you can crop image and send to OCR  , false detected will return no text :)
    cropped = img_final[y :y +  h , x : x + w]

    s = file_name + '/crop_' + str(index) + '.jpg' 
    cv2.imwrite(s , cropped)
    index = index + 1

    '''
# write original image with added contours to disk
cv2.imshow('captcha_result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()