import cv2
import numpy as np
import json

def getColor(img_path, colorTbl):
	im = cv2.imread(img_path)
	h, w, c = im.shape

	cReg = im[int(0.45*h):int(0.55*h), int(0.45*w):int(0.55*w)]

	rgbAvg = [np.mean(cReg[:,:,2]), np.mean(cReg[:,:,1]), np.mean(cReg[:,:,0])]

	minVal = 255 * 255 * 3
	color = None
	rgb = None

	for k in colorTbl:
		v = colorTbl[k]
		tmpVal = 0
		for i in range(3):
			tmpVal = tmpVal + (v[i] - rgbAvg[i]) * (v[i] - rgbAvg[i])

		if tmpVal < minVal:
			minVal = tmpVal
			color = k
			rgb = v

	return color, rgb


def getColorTable(ct_path):

	with open(ct_path) as jsonFile:
		colorTbl = json.load(jsonFile)

	return colorTbl


if __name__ == '__main__':
	colorTbl = getColorTable('color.json')
	print(getColorTable('color.json'))
	color, rgb = getColor('../image/img1.png', colorTbl)
	print('color => ', color)
	print('rgb => ', rgb)