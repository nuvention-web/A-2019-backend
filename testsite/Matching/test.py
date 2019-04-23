from utils import colorDetect

colorTbl = colorDetect.getColorTable('../utils/color.json')
print(colorTbl)

color, rgb = colorDetect.getColor('../image/img1.png', colorTbl)
color =  colorDetect.getColorMapping(color)
print('color => ', color)