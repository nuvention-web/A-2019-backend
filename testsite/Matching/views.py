from __future__ import absolute_import
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import os
from TRE import kb
from utils import initializeFirebase
from utils import FirebaseFunc
from utils import colorDetect
#from Matching.ML import ttt
#from Matching.ML.prediction import predict
import prediction

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

        user_name = req['user_name']
        print('user_name => ', user_name)
        user = FirebaseFunc.getUserByName(db, user_name)
        print('user_val => ', user.val())

        ### The cloth information should be extracted in ML server
        # cloth_type = req['cloth_type']
        # cloth_info = req[cloth_type]
        # color = cloth_info['color']

        ### Call the color matching algorithm
        colorTbl = colorDetect.getColorTable('./utils/color.json')
        # print('colorTbl => ', colorTbl)
        color, rgb = colorDetect.getColor('./image/img1.png', colorTbl)
        # print('color => ', color)
        color = colorDetect.getColorMapping(color)
        print('color => ', color)

        print('is it here?')
        answer_lst = prediction.predict(["collar_design_labels", "skirt_length_labels", "coat_length_labels",
                                         "lapel_design_labels", "neck_design_labels", "neckline_design_labels",
                                         "pant_length_labels", "sleeve_length_labels"], ["./image/img1.png"])
        print('answer_lst => ', answer_lst)

        req['collar_design_labels'] = answer_lst[0]['collar_design_labels']
        req['skirt_length_labels'] = answer_lst[0]['skirt_length_labels']
        req['coat_length_labels'] = answer_lst[0]['coat_length_labels']
        req['lapel_design_labels'] = answer_lst[0]['lapel_design_labels']
        req['neck_design_labels'] = answer_lst[0]['neck_design_labels']
        req['neckline_design_labels'] = answer_lst[0]['neckline_design_labels']
        req['pant_length_labels'] = answer_lst[0]['pant_length_labels']
        req['sleeve_length_labels'] = answer_lst[0]['sleeve_length_labels']

        #ttt.predict()

        colors_inside_wardrobe = []

        if 'items' not in user.val():
            data = user.val()
            t_data = {'items': {'0': {'color': color, 'img_url': img_url}}}
            data.update(t_data)
            db.child("users").child(user.key()).set(data)
        else:
            ### save the color already exists to the list
            for item in user.val()['items']:
                if item:
                    colors_inside_wardrobe.append(item['color'])

            user.val()['items'].append({'color': color, 'img_url': img_url})
            db.child("users").child(user.key()).set(user.val())

        kb_facts = kb.createKB()
        color_popularity_sorted = kb_facts['color_popularity_sorted']
        color_nogood_facts = kb_facts['color_nogood_facts']

        matchCloth = None
        ### inference part
        for colorDbClass in color_popularity_sorted:
            p1 = colorDbClass
            print('p1.fact => ', p1.fact)
            if color in p1.fact:
                if color == p1.fact[0]:
                    matchColor = p1.fact[1]
                else:
                    matchColor = p1.fact[0]

                if matchColor == '*':
                    matchColor = colors_inside_wardrobe[0]

                for item in user.val()['items']:
                    if item and item['color'] == matchColor:
                        matchCloth = item
                        break
                if matchCloth:
                    break

        print('is it here ????')

        if matchCloth == None:
            for nogood in color_nogood_facts:
                print('nogood => ', nogood)
                if color in nogood:
                    if color == nogood[0]:
                        colors_inside_wardrobe.remove(nogood[1])
                    else:
                        colors_inside_wardrobe.remove(nogood[0])

            for item in user.val()['items']:
                if item and item['color'] == colors_inside_wardrobe[0]:
                    matchCloth = item
                    break

        print('matchCloth => ', matchCloth)

        req['matchCloth'] = matchCloth

        req['colorPredict'] = color

        print('req => ', req)
        # print('color_popularity_sorted => ', color_popularity_sorted)
        # print('color_nogood_facts => ', color_nogood_facts)

        # jo = json.dumps(request.body)

        return HttpResponse(json.dumps(req))
