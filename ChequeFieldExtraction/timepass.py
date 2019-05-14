if __name__ == "__main__":
	import utils
	import sys
	import cv2
	import os
	import glob
	import numpy as np

	image = np.zeros((10, 10), np.uint8)
	image.fill(255)
	cv2.imshow("abc", image)
	cv2.waitKey()