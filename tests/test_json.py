from google.oauth2.service_account import Credentials
import json

creds = Credentials.from_service_account_file("credentials.json")
with open("credentials.json") as f:
    info = json.load(f)
print("Service account email:", info.get("client_email"))
