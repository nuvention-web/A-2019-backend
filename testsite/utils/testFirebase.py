# import firebase_admin
# from firebase_admin import credentials, firestore

# cred = credentials.Certificate('../profashion-firebase-adminsdk-vf1ta-35e8761196.json')
# prof_app = firebase_admin.initialize_app(cred)
# db = firestore.client()

# print(prof_app.project_id)

# doc_ref = db.collection('profashion').document('users')

# try:
#    doc = doc_ref.get('users')
#    print('document data : {}'.format(doc.to_dict()))
# except:
#    print('document is not found!')

import pyrebase

config = {
    "apiKey": "AIzaSyBR_Uy5rZW-lvfq_aaDzM-yZP3H_NWCMSg",
    "authDomain": "profashion.firebaseapp.com",
    "databaseURL": "https://profashion.firebaseio.com",
    "storageBucket": "profashion.appspot.com",
    "serviceAccount": "../profashion-firebase-adminsdk-vf1ta-35e8761196.json"
}

firebase = pyrebase.initialize_app(config)
print('firebase => ', firebase)

db = firebase.database()
all_users = db.child("users").get()

"""
for user in all_users.each():
    print('user => ', user)
    print('user key => ', user.key())
    print('user value => ', user.val())
    json = user.val()
    if 'items' in json:
        json = json['items']
        print('json => ', json)
"""

tmp_user = None

for user in all_users.each():
    if 'Cathy' == user.val()['username']:
        print('success!!!')
        tmp_user = user
        break

print('tmp_user => ', tmp_user)

if 'items' not in tmp_user.val():
    data = tmp_user.val()

    idx = 0

    t_data = {'items': {idx: {'color': 'red', 'img_url': 'www.google.com'}}}
    data.update(t_data)
    print('data => ', data)
    db.child("users").child("1").set(data)
else:
    data = user.val()['items']
    user.val()['items'].append({'color': 'yellow', 'img_url': 'www.kfc.com'})
    print('data => ', data)
    #db.child("users").child(user.key()).set(data)