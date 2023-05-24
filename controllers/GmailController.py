from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from bs4 import BeautifulSoup

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailController:

    def __init__(self) -> None:
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def getTitles(self):
        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=self.creds)
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

    def fetch_emails(self, num_emails):
        try:
            # fetch email messages
            service = build('gmail', 'v1', credentials=self.creds)
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
                if 'parts' in payload:
                    #print(payload)
                    #print()
                    if 'parts' in payload['parts'][0]: parts = payload['parts'][0]['parts']
                    else: parts = payload['parts']
                    data = parts[0]['body']['data']
                else:
                    data = payload['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)
                print(decoded_data)
                soup = BeautifulSoup(decoded_data , "lxml")
                body = soup.body()
                print('Subject:', subject)
                print(len(body))
                #print('Body:', body)
                html_string = ''.join(str(x) for x in body)
                soup = BeautifulSoup(html_string, 'lxml')
                print()
                text = soup.get_text()
                print(text)
                print()
                print()

        except HttpError as error:
            print(f'An error occurred: {error}')
