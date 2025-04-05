from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None

    # Verifica se o token já existe
    if os.path.exists('config/token.json'):
        creds = Credentials.from_authorized_user_file('config/token.json', SCOPES)

    # Se não houver credenciais válidas, faz login e salva o token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Atualiza o token expirado
        else:
            flow = InstalledAppFlow.from_client_secrets_file("config/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Salva o token para reutilizar depois
        with open('config/token.json', 'w') as token:
            token.write(creds.to_json())

    # Retorna o serviço com credenciais autenticadas
    service = build('gmail', 'v1', credentials=creds)
    return service
