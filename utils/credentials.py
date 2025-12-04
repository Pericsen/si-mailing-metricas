import os
import re
import sys
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")

def get_creds():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_PATH,
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
    )

    if not creds:
        print('Unable to authenticate using service account key.')
        sys.exit()
    else:
        print('Credenciales ok')

    return creds