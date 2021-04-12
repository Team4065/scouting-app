import os
import errno
from firebase_admin import credentials, firestore, initialize_app
import dotenv
from dataclasses import asdict
import re
import json

from flask.json import jsonify

pattern = re.compile('[\\\\/]') # 

cred = os.environ.get('credentials') # See if credentials are in the environment

if cred:
    cred = json.loads(cred)
    cred = credentials.Certificate(cred)
else: 
    path = dotenv.get_key('.env', 'CERTIFICATE_PATH') # Path relative to .env
    path_list = [*pattern.split(os.getcwd()), *pattern.split(path)]
    absolute_path = '\\'.join([x for x in path_list if x]) # Join path and ensure no list indicies are empty strings

    if not os.path.exists(absolute_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), absolute_path)

    cred = credentials.Certificate(absolute_path)

app = initialize_app(cred)
db = firestore.client(app)

users_ref = db.collection('users')

def get_user_by_email(email):
    query = users_ref.where('email', '==', email).limit(1)
    docs = list(query.stream())

    if len(docs) < 1:
        return None 

    doc = docs[0]

    if not doc.exists:
        return None
    
    return {**doc.to_dict(), 'uid': doc.id}

def get_users_by_role(role):
    query = users_ref.where('role', '==', role)
    users = list(
        map(
            lambda u: u.to_dict(),
            list(query.stream())
        )
    ) # Convert list of firestore.DocumentSnapshot to a list of dictionaries


    return users

def user_exists(uid):
  user = users_ref.document(uid).get()

  return user.exists

def add_user(user):
    print(dir(user))
    d = asdict(user)
    uid = d['uid']

    d.pop('uid', None)
    d.pop('authenticated', None)

    users_ref.document(uid).set(d)