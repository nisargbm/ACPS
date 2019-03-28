import pytesseract
import PIL
import cv2
import numpy as np

import csv

def test(file_name, img):
    # text = pytesseract.image_to_string(img)
    # config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
    #text = pytesseract.image_to_data(img, lang=None, config='', nice=0, output_type=Output.STRING)
    text = text.replace(" ", "")
    print(text)
    # myData = [file_name, str(text)]
    # myFile = open('accountNumber.csv', 'a')
    # with myFile:  
    #   writer = csv.writer(myFile)
    #   writer.writerow(myData)
    # cv2.imshow('display_image', img)
    # cv2.waitKey()
    return text


if __name__ == "__main__":
    filename = './temp1/amount/Cheque 309112.tif'
    img = cv2.imread(filename,0)


    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8)
    height, width = img.shape[:2]

    ret,img = cv2.threshold(img,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    
    # while( not done):
    #     eroded = cv2.erode(img,element)
    #     temp = cv2.dilate(eroded,element)
    #     temp = cv2.subtract(img,temp)
    #     skel = cv2.bitwise_or(skel,temp)
    #     img = eroded.copy()
     
    #     zeros = size - cv2.countNonZero(img)
    #     if zeros==size:
    #         done = True
 

    skel = img 
    skel = 255 - skel
    cv2.imshow("skel",skel)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # text = pytesseract.image_to_string(PIL.Image.open(filename))
    text = pytesseract.image_to_string(skel, lang='eng', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789,-')
    print(text)
    cv2.imshow('display_image', skel)
    cv2.waitKey()