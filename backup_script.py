import os
import os.path

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  service = build("driveactivity", "v2", credentials=creds)

  # Call the Drive Activity API
  try:
    service = build("drive", "v3", credentials=creds)

    response = service.files().list(
      q = "name='BackupFolder2024' and mimeType='application/vnd.google-apps.folder'",
      spaces = 'drive'
    ).execute()

    if not response['files']:
      file_metadata = {
        "name":"BackUpFolder2024",
        "mimeType":"application/vnd.google-apps.folder"
      }

      file = service.files().create(body = file_metadata, fields="id").execute()

      folder_id  = file.get('id')
    else:
      folder_id = response['files'][0]['id']

    for file in os.listdir('backupfiles'):
      file_metadata = {
        "name": file,
        "parents":[folder_id]
      }

      media = MediaFileUpload(f"backupfiles/{file}")
      upload_file = service.files().create(body = file_metadata,
                                           media_body = media,
                                           fields = "id").execute()
      
      print("Backed up files:" + file)
    
  except HttpError as error:
    print(f"An error occurred: {error}")



if __name__ == "__main__":
  main()