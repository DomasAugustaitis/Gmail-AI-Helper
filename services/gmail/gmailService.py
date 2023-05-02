from __future__ import print_function

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from bs4 import BeautifulSoup
import lxml
from services.openAI import chatGptService

def getLabels(creds):
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:    
            print('Labels:')
            for label in labels:
                print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

def getEmails(creds, num_emails):
    try:
        # fetch email messages from Primary tab only
        service = build('gmail', 'v1', credentials=creds)
        query = 'category:primary'
        messages = service.users().messages().list(userId='me', q=query, maxResults=num_emails).execute()

        # iterate through messages and print subject and body
        for message in messages['messages']:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']
            subject = ''
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
            print('Subject:', subject)

            try:
                if 'parts' in payload:
                    parts = payload['parts']
                    data = parts[0]['body']['data']
                else:
                    data = payload['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)
                soup = BeautifulSoup(decoded_data , "lxml")
                body = soup.text
                #soup = BeautifulSoup(body, 'html.parser')
                #body = soup.body()
                print()
                print()
                chatGptService.summariseEmail(body)
                print()
                print()
                print('Body:', body)
            except Exception as bodyError:
                print(f'Error occured parsing the email body: {bodyError}')
                print()
                print()
            
            
    except Exception as error:
        print(f'An error occurred: {error}')

def searchEmails(creds, keywords, num_emails):
    try:
        # construct query string to search for emails containing all specified keywords
        service = build('gmail', 'v1', credentials=creds)
        query = ' '.join(['"' + keyword + '"' for keyword in keywords])
        messages = service.users().messages().list(userId='me', q=query, maxResults=num_emails).execute()

        # iterate through messages and print message snippet
        for message in messages['messages']:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(msg['snippet'])
    except HttpError as error:
        print(f'An error occurred: {error}')