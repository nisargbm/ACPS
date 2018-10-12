import pytesseract
import PIL
import cv2

filename = './temp/5186.jpg'
img = cv2.imread(filename)
text = pytesseract.image_to_string(PIL.Image.open(filename))
print(text)
cv2.imshow('display_image', img)
cv2.waitKey()