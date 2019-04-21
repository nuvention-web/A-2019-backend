from firebase import firebase
# Import database module.

### Current thought, is get recognition result in backend, and store "color" result inside database.

my_firebase_auth_token = "AAAASX632B4:APA91bF70GqvH_3uouS0MtpDoiS7g9UTnXAC8-X-HryZgAIKq8hiZ9ktbWBlitsUYrsbwsAGwCzD2QjsPI5ZkSqatAYtQFkLtODhDEH0UE3RFzSiH9CWGLOHv_JFFXXWpIXvjJ0MbYAr"
firebase = firebase.FirebaseApplication('https://fashionai-c4099.firebaseio.com', my_firebase_auth_token)
result = firebase.get('/Wardrobe', None)

print('result => ', result)