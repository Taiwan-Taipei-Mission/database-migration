#Python native imports
import os
import sys
import json
import csv
import time
from datetime import datetime
#Python dependencies (to run the code, pip install these onto your pc)
import firebase_admin
from firebase_admin import credentials, firestore
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Log into Gdrive
gauth = GoogleAuth()
gauth.LoadCredentialsFile("credentials.json")
if gauth.credentials is None:
	gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
	gauth.Refresh()
else:
	gauth.Authorize()
gauth.SaveCredentialsFile("credentials.json")
drive = GoogleDrive(gauth)
#download the file
classdatabase = drive.CreateFile({'id': '1Q2xMx_TJwndYrEB2cyX4MK3dchMkvuUPPD6xuU4Osfw'})
classdatabase.FetchMetadata()
classdatabase.GetContentFile('classdatabase.csv', mimetype='text/csv')
referrals = open('classdatabase.csv', "r", newline='', encoding='utf-8')
referral1 = csv.DictReader(referrals)


#Give a starting value for the loop name.
loop_name = 1

#Firestooooooorm ACTIVATE! (firestorm auth)
cred = credentials.Certificate('./taiwaneng-alpha-firebase-adminsdk-0rxki-afd1fa7bc4.json')
applet = firebase_admin.initialize_app(cred)
db = firestore.client()

#Firestorm loop
for referral in referral1: #access dict with ref info
        loop_str = str(loop_name)
        #doc_ref = db.document(u'ReferralDB/{}/Referrals/{}--{}/{}'.format(referral[u'Select-5'], loop_str, referral[u'Text-8'],referral[u'Text-6']))
        doc_ref = db.document(u'ReferralDB/{}_data/refcollection/{}-referralsheet'.format(referral['Select-5'], loop_str))
		#Make Correct phone numbers
		doc_ref.set({
            u'Submitted on': referral[u'Submitted On'],
            u'English Name': referral[u'Text-8'],
            u'Chinese name': referral[u'Text-6'],
            u'Gender': referral[u'Radio-2'],
            u'Location': referral[u'Select-5'],
            u'LINE ID': referral[u'LINE ID'],
            u'Phone Number': referral[u'Text-9'],
            u'Class Level': referral[u'Radio-3'],
            u'Questions, Comments, and Concerns': referral[u'Textarea-10'],
            u'Do they want the gospel?': referral[u'Radio-4'],
            u'What source did they come from?': referral[u'Source']
        })
        print("Referral successfully saved to {}".format(referral['Select-5']))
        loop_name += 1
referrals.close()
#retrieve data
try:
    doc = doc_ref.get()
    print(u'Document data: {}'.format(doc.to_dict()))
    # do something with retrieved data
except google.cloud.exceptions.NotFound:
    print(u'No such document exists!')
