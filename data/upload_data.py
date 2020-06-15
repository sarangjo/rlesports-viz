import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
default_app = firebase_admin.initialize_app()

db = firestore.client()

doc_ref = db.collection(u'players').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})
