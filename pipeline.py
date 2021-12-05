import os
import requests
import firebase_admin
from firebase_admin import db

# DB Setup
cred_info = {
    "type": "service_account",
    "project_id": os.environ['PROJECT_ID'],
    "private_key_id": os.environ['API_KEY'],
    "private_key": os.environ['PRIVATE_KEY'],
    "client_email": os.environ['EMAIL'],
    "client_id": os.environ['ID'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ['x509']
}
print(cred_info)

cred = firebase_admin.credentials.Certificate(cred_info)
app = firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ['DATABASE_URL']
})
ref = db.reference("/")

# Read
response = requests.get(
    f"https://na.whatismymmr.com/api/v1/summoner?name=${os.environ['SUMMONER']}")
aram_data = response.json()['ARAM']

# Write
ref.child(str(aram_data['timestamp'])).set({'mmr': aram_data['avg'], 'percentile': aram_data.get(
    'percentile', 0), 'rank': aram_data.get('closestRank', '')})
