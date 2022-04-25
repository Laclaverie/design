# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:13:58 2021

@author: Julien
"""

# pip install pyrebase4
import pyrebase

from modules.variables import REMOTE_FOLDER, LOCAL_FOLDER

config = {
    "apiKey": "AIzaSyCA6wqd1CbI4ALT0IqMZJf5Rykh3HG4xXw",
    "authDomain": "biennale-742d2.firebaseapp.com",
    "databaseURL": "https://biennale-742d2-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "biennale-742d2",
    "storageBucket": "biennale-742d2.appspot.com",
    "messagingSenderId": "488997263871",
    "appId": "1:488997263871:web:186e112436cde18f756fca"
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()


def upload_on_firebase(name):
    storage.child(REMOTE_FOLDER + name).put(LOCAL_FOLDER + name)
