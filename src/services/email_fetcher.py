from googleapiclient.discovery import build
from services.gmail_service import get_gmail_service
from collections import defaultdict
import progressbar  # Adiciona isso

def count_emails_by_sender():
    """Conta a quantidade de e-mails por remetente, buscando até x e-mails."""
    service = get_gmail_service()
    senders_count = defaultdict(int)  # Dicionário para contar os e-mails por remetente

    # Busca inicial (primeiros 100 e-mails)
    results = service.users().messages().list(userId="me", maxResults=100).execute()
    messages = results.get("messages", [])
    total_emails = len(messages)

    # Paginação até atingir x e-mails
    while results.get("nextPageToken") and total_emails < 150:
        page_token = results["nextPageToken"]
        results = service.users().messages().list(userId="me", maxResults=100, pageToken=page_token).execute()
        new_messages = results.get("messages", [])
        
        if total_emails + len(new_messages) > 150:
            new_messages = new_messages[:150 - total_emails]
        
        messages.extend(new_messages)
        total_emails += len(new_messages)

    with progressbar.ProgressBar(max_value=len(messages)) as bar:
        for i, msg in enumerate(messages):
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = msg_data["payload"].get("headers", [])

            sender = "Desconhecido"
            for header in headers:
                if header["name"] == "From":
                    sender = header["value"]

            senders_count[sender] += 1
            bar.update(i)

    return senders_count
