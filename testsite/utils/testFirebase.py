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

db = firebase.database()
all_users = db.child("users").get()


tmp_user = None

for user in all_users.each():
    print('user key???? = ', user.key())

users_by_name = db.child("users").order_by_child("username").equal_to("Cathy").get()
print('userByName => ', users_by_name.key())
for user in users_by_name.each():
    print('user key => ', user.key())
    print('user value => ', user.val())