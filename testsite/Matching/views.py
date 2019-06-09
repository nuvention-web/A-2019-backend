from __future__ import absolute_import
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import os
from utils import initializeFirebase
from utils import colorDetect
import prediction
import math
import random
from utils import weather
from utils import clothMatching

def urllib_download(IMAGE_URL, USER_KEY):
    from urllib.request import urlretrieve
    urlretrieve(IMAGE_URL, './image/' + USER_KEY + '.png')


class ClothInfo(APIView):
    def post(self, request, *args, **kwargs):
        jsonstr = str(request.body, 'utf-8')
        req = json.loads(jsonstr)
        os.makedirs('./image/', exist_ok=True)

        ### Initialize Firebase, should use cache to store that later.
        db = initializeFirebase.initializeFB()

        dbKey = req['dbkey']
        user = None
        for tuser in db.child("users").get():
            if tuser.key() == dbKey:
                user = tuser
                break

        img_url = req['img_url']
        urllib_download(img_url, user.key())

        clothType = req['type']
        if clothType == 'tops':
            matchType = 'bottoms'
        else:
            matchType = 'tops'

        ### Call the color matching algorithm
        colorTbl = colorDetect.getColorTable('./utils/color.json')
        color, rgb = colorDetect.getColor('./image/' + user.key() + '.png', colorTbl)
        hsv = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])

        print('#### Start ML Part ####')
        answer_lst = prediction.predict(["collar_design_labels", "skirt_length_labels", "coat_length_labels",
                                         "lapel_design_labels", "neck_design_labels", "neckline_design_labels",
                                         "pant_length_labels", "sleeve_length_labels"], ["./image/"+ user.key() +".png"])
        print('answer_lst => ', answer_lst)

        req['labels'] = {
            'collar_design_labels': answer_lst[0]['collar_design_labels'],
            'skirt_length_labels': answer_lst[0]['skirt_length_labels'],
            'coat_length_labels': answer_lst[0]['coat_length_labels'],
            'lapel_design_labels': answer_lst[0]['lapel_design_labels'],
            'neck_design_labels': answer_lst[0]['neck_design_labels'],
            'neckline_design_labels': answer_lst[0]['neckline_design_labels'],
            'pant_length_labels': answer_lst[0]['pant_length_labels'],
            'sleeve_length_labels': answer_lst[0]['sleeve_length_labels']
        }
        ############### ML Part End ################

        ### Matching Clothes ALG
        temperature = weather.getWeatherInfo()
        req['matchCloth'] = clothMatching.selectMatchCloth(user, temperature, hsv, matchType, colorTbl)

        req['labels']['colorPredict'] = color

        print('req => ', req)

        return HttpResponse(json.dumps(req))

class RecommendPurchase(APIView):
    def post(self, request, *args, **kwargs):
        jsonstr = str(request.body, 'utf-8')
        req = json.loads(jsonstr)

        db = initializeFirebase.initializeFB()

        dbKey = req['dbkey']
        user = None
        for tuser in db.child("users").get():
            if tuser.key() == dbKey:
                user = tuser
                break

        clothID = req['clothID']
        cloth = None
        for item in user.val()['items'].items():
            if item[0] == clothID:
                cloth = item[1]

        clothType = cloth['type']
        if clothType == 'tops':
            matchType = 'bottoms'
        else:
            matchType = 'tops'

        colorTbl = colorDetect.getColorTable('./utils/color.json')
        clothColor = cloth['color']
        if clothColor in colorTbl:
            clothColorRGB = colorTbl[clothColor]
        else:
            clothColorRGB = None

        hsv = None
        if clothColorRGB:
            hsv = colorDetect.CalHSV(clothColorRGB[0], clothColorRGB[1],
                                     clothColorRGB[2])
        maxScore = 0.0
        matchCloth = None
        ### save the color already exists to the list
        for item in user.val()['items'].values():
            if item and item['type'] == matchType:
                tcolor = item['color']
                if tcolor != None:
                    rgb = colorTbl[tcolor]
                hsv2 = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])
                score = colorDetect.CalColorGrade(hsv, hsv2)
                if score > maxScore:
                    maxScore = score
                    matchCloth = item

        req['matchCloth'] = matchCloth

        matchColor = matchCloth['color']
        if matchColor in colorTbl:
            matchColorRGB = colorTbl[matchColor]
        else:
            matchColorRGB = None

        minDistance = 1<<31
        allPossibleClothes = []

        for item in db.child("purchase").get():
            if item.val() == None:
                continue
            itemColor = item.val()['color']
            if itemColor in colorTbl:
                itemRGB = colorTbl[itemColor]
            else:
                itemRGB = None

            distance = math.sqrt((matchColorRGB[0] - itemRGB[0]) ** 2 +\
                                 (matchColorRGB[1] - itemRGB[1]) ** 2 +\
                                 (matchColorRGB[2] - itemRGB[2]) ** 2)
            if distance < minDistance and item.val()['type'] == matchType:
                minDistance = distance
                allPossibleClothes.clear()
                allPossibleClothes.append(item.val())
            elif distance == minDistance and item.val()['type'] == matchType:
                allPossibleClothes.append(item.val())

        if allPossibleClothes != []:
            req['recommendPurchase'] = random.choice(allPossibleClothes)
        else:
            req['recommendPurchase'] = None

        return HttpResponse(json.dumps(req))

class WeatherInfo(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(weather.getWeatherInfo()))