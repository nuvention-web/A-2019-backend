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

def getColorMapping(color):
	json = {
		'red': ['LightPink', 'Pink', 'Crimson', 'HotPink', 'DeepPink', 'Orchid', 'Thistle', 'Plum', 'Magenta', 'DarkMagenta',
				'PeachPuff', 'LightSalmon', 'OrangeRed', 'DarkSalmon', 'Tomato', 'MistyRose', 'LightCoral',
				'RosyBrown', 'IndianRed', 'Red', 'FireBrick', 'DarkRed'],
		'purple': ['LavenderBlush', 'PaleVioletRed', 'MediumVioletRed', 'Violet', 'Purple', 'MediumOrchid', 'DarkViolet', 'DarkOrchid',
				   'Indigo', 'BlueViolet', 'MediumPurple' ],
		'blue': ['MediumSlateBlue', 'SlateBlue', 'DarkSlateBlue', 'Lavender', 'Blue', 'MediumBlue', 'MidnightBlue', 'DarkBlue',
				 'Navy', 'RoyalBlue', 'CornflowerBlue', 'LightSteelBlue', 'DodgerBlue',
				 'AliceBlue', 'SteelBlue', 'LightSkyBlue', 'SkyBlue', 'DeepSkyBlue', 'LightBlue', 'PowderBlue',
				 'CadetBlue', 'Azure', 'PaleTurquoise', 'Aqua', 'DarkTurquoise', 'MediumTurquoise',
				 'Aquamarine', 'MediumAquamarine'],
		'gray': ['SlateGray', 'LightSlateGray', 'DarkSlateGray', 'Gainsboro', 'LightGrey', 'Silver',
				'DarkGray', 'Gray', 'DimGray', 'Black'],
		'green': ['LightCyan', 'Cyan', 'DarkCyan', 'Teal', 'LightSeaGreen', 'Turquoise', 'MediumSpringGreen',
				  'SpringGreen', 'MediumSeaGreen', 'SeaGreen', 'LightGreen', 'PaleGreen',
				  'DarkSeaGreen', 'LimeGreen', 'Lime', 'ForestGreen', 'Green', 'DarkGreen', 'Chartreuse',
				  'LawnGreen', 'GreenYellow', 'DarkOliveGreen', 'YellowGreen', 'OliveDrab', 'Olive'],
		'white': ['GhostWhite', 'MintCream', 'Honeydew', 'Beige', 'Ivory', 'FloralWhite', 'OldLace', 'BlanchedAlmond',
				  'NavajoWhite', 'AntiqueWhite', 'Snow', 'White', 'WhiteSmoke', ],
		'yellow': ['LightGoldenrodYellow', 'LightYellow', 'Yellow', 'DarkKhaki', 'LemonChiffon', 'PaleGoldenrod',
				   'Khaki', 'Gold', 'Cornsilk', 'Goldenrod', 'DarkGoldenrod', 'Wheat', 'Moccasin',
				   'Orange', 'PapayaWhip', 'Tan', 'BurlyWood', 'Bisque', 'DarkOrange', 'Linen', 'Peru',
				   'Seashell', 'Sienna', 'Salmon', 'Maroon'],
		'brown': ['Chocolate', 'SandyBrown', 'SaddleBrown', 'Coral', 'Brown', ]
	}

	for key, value in json.items():
		if color in value:
			return key

if __name__ == '__main__':
	colorTbl = getColorTable('color.json')
	print(getColorTable('color.json'))
	color, rgb = getColor('../image/img1.png', colorTbl)
	print('color => ', color)
	print('rgb => ', rgb)
	print(getColorMapping(color))