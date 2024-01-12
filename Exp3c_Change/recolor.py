import cv2, os
import numpy as np

inpath = '/Users/yichen/Downloads/images_merged/' # image size 400 H x 1000 W 
outpath = '/Users/yichen/Downloads/images_recolored/'
filenames = [f for f in os.listdir(inpath) if os.path.isfile(os.path.join(inpath, f))]

def increase_brightness(img, mask, saturation=100, value=100, maxvalue=220):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h,s,v = cv2.split(hsv)

	# increase brightness to max 255
	if np.max(v) > maxvalue:
		print('skip value')
		return img
	lim = 255 - value
	v[(mask>0) & (v<=lim)] += value
	v[(mask>0) & (v>lim)] = 255
	assert np.max(v)>=maxvalue

	# setting saturation
	assert np.max(s)==255
	# s[(mask>0) & (s>=saturation)] -= saturation
	# s[(mask>0) & (s<0)] = 0
	s[mask>0] = saturation

	final_hsv = cv2.merge((h,s,v))
	img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return img


def add_white_boundary(img, halfbar=5):
	'''
	add a vertical white bar in the middle of the image, with width halfbar*2
	'''
	height, width, channels = img.shape
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h,s,v = cv2.split(hsv)
	h[:, width//2-halfbar:width//2+halfbar] = 0
	s[:, width//2-halfbar:width//2+halfbar] = 0
	v[:, width//2-halfbar:width//2+halfbar] = 255
	final_hsv = cv2.merge((h,s,v))
	img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return img	



for file in filenames:
	initimg = cv2.imread(os.path.join(inpath, file))
	hsv = cv2.cvtColor(initimg, cv2.COLOR_BGR2HSV)
	black_lo = np.array([0, 0, 0])
	black_hi = np.array([5, 5, 5])
	mask = cv2.inRange(hsv, black_lo, black_hi)
	mask = cv2.bitwise_not(mask)
	newimg = increase_brightness(initimg, mask)
	cv2.imwrite(os.path.join(outpath, file), newimg)

