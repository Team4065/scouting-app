import os
import errno
from firebase_admin import credentials, firestore, initialize_app
import dotenv
from dataclasses import asdict
import re

pattern = re.compile('[\\\\/]') # 

path = dotenv.get_key('.env', 'CERTIFICATE_PATH') # Path relative to .env
path_list = [*pattern.split(os.getcwd()), *pattern.split(path)]
absolute_path = '\\'.join([x for x in path_list if x]) # Join path and ensure no list indicies are empty strings

if not os.path.exists(absolute_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), absolute_path)

cred = credentials.Certificate(absolute_path)
app = initialize_app(cred)
db = firestore.client(app)

users = db.collection('users')

def get_user_by_email(email):
    query = users.where('email', '==', email).limit(1)
    docs = list(query.stream())

    if len(docs) < 1:
        return None 

    doc = docs[0]

    if not doc.exists:
        return None
    
    return {**doc.to_dict(), 'uid': doc.id}

def user_exists(uid):
  user = users.document(uid).get()

  return user.exists

def add_user(user):
    print(dir(user))
    d = asdict(user)
    uid = d['uid']

    d.pop('uid', None)
    d.pop('authenticated', None)

    users.document(uid).set(d)