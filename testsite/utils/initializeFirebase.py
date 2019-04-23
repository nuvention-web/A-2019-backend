import pyrebase
from utils import FirebaseConfig

def initializeFB():
    firebase = pyrebase.initialize_app(FirebaseConfig.config)
    #print('firebase => ', firebase)

    db = firebase.database()
    return db

if __name__ == '__main__':
    initializeFB()