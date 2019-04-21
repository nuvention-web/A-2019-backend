import json
from django.http import HttpResponse
from rest_framework.views import APIView
import os
from TRE import kb

def urllib_download(IMAGE_URL):
    from urllib.request import urlretrieve
    urlretrieve(IMAGE_URL, './image/img1.png')

# Create your views here.
class Recommendation(APIView):
    def post(self, request, *args, **kwargs):
        jsonstr = str(request.body, 'utf-8')
        req = json.loads(jsonstr)
        os.makedirs('./image/', exist_ok=True)

        try:
            if 'img_url' in req:
                urllib_download(req['img_url'])

            kb_facts = kb.createKB()
            color_popularity_sorted = kb_facts['color_popularity_sorted']
            color_nogood_facts = kb_facts['color_nogood_facts']

            ### The cloth information should be extracted in ML server
            cloth_type = req['cloth_type']
            cloth_info = req[cloth_type]
            color = cloth_info['color']
            

        except:
            print('An exception occurred!')


        #jo = json.dumps(request.body)

        return HttpResponse(jsonstr)
