from googleapiclient.discovery import build
from services.gmail_service import get_gmail_service
from collections import defaultdict
import progressbar  


def delete_emails_by_sender(target_email, limit=3000):
    service = get_gmail_service()
    deleted_count = 0

    results = service.users().messages().list(userId="me", maxResults=100).execute()
    messages = results.get("messages", [])
    total_fetched = 0

    while results.get("nextPageToken") and total_fetched < limit:
        page_token = results["nextPageToken"]
        results = service.users().messages().list(userId="me", maxResults=100, pageToken=page_token).execute()
        new_messages = results.get("messages", [])

        if total_fetched + len(new_messages) > limit:
            new_messages = new_messages[:limit - total_fetched]

        messages.extend(new_messages)
        total_fetched += len(new_messages)

    # Deleta e-mails que vieram do e-mail alvo
    with progressbar.ProgressBar(max_value=len(messages)) as bar:
        for i, msg in enumerate(messages):
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = msg_data["payload"].get("headers", [])

            sender = ""
            for header in headers:
                if header["name"] == "From":
                    sender = header["value"]
                    break

            if target_email in sender:
                service.users().messages().trash(userId="me", id=msg["id"]).execute()
                deleted_count += 1
                bar.update(i)
    return deleted_count
