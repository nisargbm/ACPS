import cv2
import numpy as np
import utils
 
img = cv2.imread('./temp1/amount/Cheque 309160.tif',0)
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
 

# skel = img 
cv2.imshow("skel",skel)
cv2.waitKey(0)
cv2.destroyAllWindows()

skel = cv2.dilate(skel,element)
cv2.imshow("skel",skel)
cv2.waitKey(0)
cv2.destroyAllWindows()
# ret,thresh = cv2.threshold(skel,127,255,0)
# im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)

_, contours, _ = cv2.findContours(skel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for contour in contours:
    area = cv2.contourArea(contour)
    x, y, w, h = cv2.boundingRect(contour)

    if w > width//100 and h > height//3:
    # cv2.drawContours(skel, contour, -1, (255, 255, 255), 3)
        cv2.rectangle(skel, (x , y), (x + w , y + h), (255, 255, 255), 2)
        crop_img = skel[y : y + h, x : x + w]
        utils.display_image('captcha_result', crop_img)

cv2.imshow("skel",skel)
cv2.waitKey(0)
cv2.destroyAllWindows()