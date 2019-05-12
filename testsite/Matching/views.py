from __future__ import absolute_import
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import os
from TRE import kb
from utils import initializeFirebase
from utils import colorDetect
import prediction
import math

def urllib_download(IMAGE_URL):
    from urllib.request import urlretrieve
    urlretrieve(IMAGE_URL, './image/img1.png')


# Create your views here.
class Recommendation(APIView):

    def post(self, request, *args, **kwargs):
        jsonstr = str(request.body, 'utf-8')
        req = json.loads(jsonstr)
        os.makedirs('./image/', exist_ok=True)

        ### Initialize Firebase, should use cache to store that later.
        db = initializeFirebase.initializeFB()

        img_url = req['img_url']
        urllib_download(img_url)

        dbKey = req['dbkey']
        user = None
        for tuser in db.child("users").get():
            if tuser.key() == dbKey:
                user = tuser
                break
        print('user_val => ', user.val())

        clothType = req['type']
        if clothType == 'tops':
            matchType = 'bottoms'
        else:
            matchType = 'tops'


        ### Call the color matching algorithm
        colorTbl = colorDetect.getColorTable('./utils/color.json')
        color, rgb = colorDetect.getColor('./image/img1.png', colorTbl)
        hsv = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])


        print('#### Start ML Part ####')
        answer_lst = prediction.predict(["collar_design_labels", "skirt_length_labels", "coat_length_labels",
                                         "lapel_design_labels", "neck_design_labels", "neckline_design_labels",
                                         "pant_length_labels", "sleeve_length_labels"], ["./image/img1.png"])
        print('answer_lst => ', answer_lst)

        req['labels'] = {
            'collar_design_labels' : answer_lst[0]['collar_design_labels'],
            'skirt_length_labels' : answer_lst[0]['skirt_length_labels'],
            'coat_length_labels' : answer_lst[0]['coat_length_labels'],
            'lapel_design_labels' : answer_lst[0]['lapel_design_labels'],
            'neck_design_labels' : answer_lst[0]['neck_design_labels'],
            'neckline_design_labels' : answer_lst[0]['neckline_design_labels'],
            'pant_length_labels' : answer_lst[0]['pant_length_labels'],
            'sleeve_length_labels' : answer_lst[0]['sleeve_length_labels']
        }
        ############### ML Part End ################
        

        if 'items' not in user.val():
            data = user.val()
            t_data = {'items': {'0': {'color': color, 'img_url': img_url, 'type': clothType}}}
            data.update(t_data)
            db.child("users").child(user.key()).set(data)
        else:
            maxScore = 0.0
            matchCloth = None

            ### save the color already exists to the list
            for item in user.val()['items']:
                if item and item['type'] == matchType:
                    # colors_inside_wardrobe.append(item['color'])
                    tcolor = item['color']
                    rgb = colorTbl[tcolor]
                    hsv2 = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])
                    score = colorDetect.CalColorGrade(hsv, hsv2)
                    if score > maxScore:
                        maxScore = score
                        matchCloth = item

            user.val()['items'].append({'color': color, 'img_url': img_url, 'type': clothType})
            db.child("users").child(user.key()).set(user.val())

        req['matchCloth'] = matchCloth

        req['labels'] = {}
        req['labels']['colorPredict'] = color

        print('req => ', req)

        return HttpResponse(json.dumps(req))


class ClothInfo(APIView):
    def post(self, request, *args, **kwargs):
        jsonstr = str(request.body, 'utf-8')
        req = json.loads(jsonstr)
        os.makedirs('./image/', exist_ok=True)

        ### Initialize Firebase, should use cache to store that later.
        db = initializeFirebase.initializeFB()

        img_url = req['img_url']
        urllib_download(img_url)

        dbKey = req['dbkey']
        user = None
        for tuser in db.child("users").get():
            if tuser.key() == dbKey:
                user = tuser
                break
        print('user_val => ', user.val())

        clothType = req['type']
        if clothType == 'tops':
            matchType = 'bottoms'
        else:
            matchType = 'tops'

        ### Call the color matching algorithm
        colorTbl = colorDetect.getColorTable('./utils/color.json')
        color, rgb = colorDetect.getColor('./image/img1.png', colorTbl)
        hsv = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])

        print('#### Start ML Part ####')
        answer_lst = prediction.predict(["collar_design_labels", "skirt_length_labels", "coat_length_labels",
                                         "lapel_design_labels", "neck_design_labels", "neckline_design_labels",
                                         "pant_length_labels", "sleeve_length_labels"], ["./image/img1.png"])
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

        maxScore = 0.0
        matchCloth = None

        ### save the color already exists to the list
        for item in user.val()['items'].values():
            if item and item['type'] == matchType:
                # colors_inside_wardrobe.append(item['color'])
                tcolor = item['color']
                rgb = colorTbl[tcolor]
                hsv2 = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])
                score = colorDetect.CalColorGrade(hsv, hsv2)
                if score > maxScore:
                    maxScore = score
                    matchCloth = item

        req['matchCloth'] = matchCloth

        req['labels']['colorPredict'] = color

        print('req => ', req)

        return HttpResponse(json.dumps(req))

class RecommendPurchase(APIView):
    def post(self, request, *args, **kwargs):
        jsonstr = str(request.body, 'utf-8')
        req = json.loads(jsonstr)

        matchColor = req['matchColor']
        colorTbl = colorDetect.getColorTable('./utils/color.json')
        if matchColor in colorTbl:
            matchColorRGB = colorTbl[matchColor]
        else:
            matchColorRGB = None

        minDistance = 1<<31
        recommendCloth = None

        db = initializeFirebase.initializeFB()
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
            if distance < minDistance:
                minDistance = distance
                recommendCloth = item.val()

        req['recommendPurchase'] = recommendCloth

        return HttpResponse(json.dumps(req))