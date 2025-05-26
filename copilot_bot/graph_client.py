import requests
import msal
import os
from dotenv import load_dotenv

load_dotenv()

class GraphClient:
    def __init__(self):
        self.client_id = os.getenv("GRAPH_CLIENT_ID")
        self.client_secret = os.getenv("GRAPH_CLIENT_SECRET")
        self.tenant_id = os.getenv("GRAPH_TENANT_ID")
        self.scope = ["https://graph.microsoft.com/.default"]
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"

    def get_token(self):
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        result = app.acquire_token_for_client(scopes=self.scope)
        return result["access_token"]

    def create_event(self, subject, start_time, end_time, attendee_email):
        token = self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        event = {
            "subject": subject,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
            "attendees": [{
                "emailAddress": {
                    "address": attendee_email,
                    "name": "John"
                },
                "type": "required"
            }]
        }
        response = requests.post(
            "https://graph.microsoft.com/v1.0/me/events",
            headers=headers,
            json=event
        )
        return response.json()
