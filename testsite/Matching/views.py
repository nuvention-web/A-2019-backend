import json
from django.http import HttpResponse
from rest_framework.views import APIView
import os
from TRE import kb
from utils import initializeFirebase
from utils import FirebaseFunc
import pyrebase

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

        try:
            img_url = req['img_url']
            urllib_download(img_url)

            user_name = req['user_name']
            print('user_name => ', user_name)
            user = FirebaseFunc.getUserByName(db, user_name)
            print('user_val => ', user.val())

            ### The cloth information should be extracted in ML server
            cloth_type = req['cloth_type']
            cloth_info = req[cloth_type]
            color = cloth_info['color']

            if 'items' not in user.val():
                data = user.val()
                t_data = {'items': {'0': {'color': color, 'img_url': img_url}}}
                data.update(t_data)
                db.child("users").child(user.key()).set(data)
            else:
                user.val()['items'].append({'color': color, 'img_url': img_url})
                db.child("users").child(user.key()).set(user.val())

            kb_facts = kb.createKB()
            color_popularity_sorted = kb_facts['color_popularity_sorted']
            color_nogood_facts = kb_facts['color_nogood_facts']
            

        except:
            print('An exception occurred!')


        #jo = json.dumps(request.body)

        return HttpResponse(jsonstr)
