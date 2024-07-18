import gspread

from oauth2client.service_account import ServiceAccountCredentials
from os import environ
from constants import Env
from datetime import datetime as dt


def get_sheet():
    PRIVATE_KEY = "\n".join(environ[Env.GOOGLE_SHEET_PRIVATE_KEY].split("\\n"))
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        {
            "type": "service_account",
            "project_id": "algo-trading-sheet",
            "private_key_id": environ[Env.GOOGLE_SHEET_PRIVATE_KEY_ID],
            "private_key": f"-----BEGIN PRIVATE KEY-----\n{PRIVATE_KEY}\n-----END PRIVATE KEY-----\n",
            "client_email": environ[Env.SERVICE_ACCOUNT],
            "client_id": environ[Env.CLIENT_ID],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/algo-trading-service-account%40algo-trading-sheet.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com",
        },
    )
    # Authenticate using the credentials
    client = gspread.authorize(credentials)

    print(f"[{dt.now()}] [Google Sheets]: Connection established")
    # Open a sheet by title
    return client.open(environ[Env.GOOGLE_SHEET])
