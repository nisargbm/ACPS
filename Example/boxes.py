import cv2
import numpy as np
import utils
import sys


def isAccountNumber(width, height, x, y, w, h):
    if((x + w < width//2) and (y>height//3 and (y + h)> height//2)):
        return True
    return False

def isDate(width, height, x, y, w, h):
    if(x > width//2 and (y + h) < height//2):
        return True
    return False

def isAmount(width, height, x, y, w, h):
    if((x > width//2) and (y > width//5 and (y + h)> (height//2 + height//5))):
        return True
    return False

def find_boxes(img_for_box_extraction_path):
# Read the image
    img = cv2.imread(img_for_box_extraction_path, 0)
    height, width = img.shape[:2]

    img = cv2.resize(img,(width//2, height//2), interpolation = cv2.INTER_AREA)
    height, width = img.shape[:2]

    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(img, 160, 255,cv2.THRESH_BINARY)
    # Invert the image
    img_bin = 255-img_bin
    utils.display_image('display_image', img_bin)
    

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(img_bin, kernel, iterations=2)  # dilate , more the iteration more the dilation
    utils.display_image('display_image', dilated)

    img_bin = dilated

    img_bin = cv2.GaussianBlur(img_bin,(5,5),0)
    utils.display_image('display_image', img_bin)

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
    utils.display_image('display_image', img_temp1)

    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=2)
    (thresh, verticle_lines_img) = cv2.threshold(verticle_lines_img, 127, 255,cv2.THRESH_BINARY)
    utils.display_image('display_image', verticle_lines_img)
    

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=2)
    utils.display_image('display_image', img_temp2)

    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=2)
    (thresh, horizontal_lines_img) = cv2.threshold(horizontal_lines_img, 127, 255,cv2.THRESH_BINARY)
    utils.display_image('display_image', horizontal_lines_img)
    

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    utils.display_image('display_image', img_final_bin)

    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    utils.display_image('display_image', img_final_bin)

    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    utils.display_image('display_image', img_final_bin)

    # Find contours for image, which will detect all the boxes
    im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    utils.display_image('display_image', im2)

    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = utils.sort_contours(contours, method="top-to-bottom")

    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        if w < width//20 or h < height//20:
            continue
        if (isAccountNumber(width, height, x, y, w, h) or isDate(width, height, x, y, w, h) or isAmount(width, height, x, y, w, h)):
            new_img = img[y:y+h, x:x+w]
            utils.display_image('display_image', new_img)
            # cv2.imwrite(dir_path+str(idx) + '.tif', new_img)
            idx = idx+1
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

    # cv2.imshow('captcha_resul', img)
    # cv2.waitKey()


dir_path = "./temp/"
img_for_box_extraction_path = str(sys.argv[1]) ##Provide argument as sample/Cheque.tif
find_boxes(img_for_box_extraction_path)


