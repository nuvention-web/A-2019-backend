import pyrebase
from utils import firebaseConfig

# Temporarily replace quote function
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

def initializeFB():
    firebase = pyrebase.initialize_app(firebaseConfig.config)
    #print('firebase => ', firebase)

    db = firebase.database()
    return db

if __name__ == '__main__':
    db = initializeFB()
    allUsers = db.child('users')
    print(allUsers.get().val())
    query = db.child("users").order_by_child("username")
    query = query.get()
    print('type allUsers => ', type(allUsers))
    print('query => ', query)