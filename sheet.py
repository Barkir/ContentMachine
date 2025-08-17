import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

SHEET_HEADERS = ["Name", "URL"]



class GoogleSheetsAPI:
    def __init__(self):
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.sheet_name = os.getenv('GOOGLE_SHEET_NAME')

        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        
        ]
        self.client = self.authenticate()
        self.worksheet = self.init_sheet()

    def authenticate(self):
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.scope
            )
            client = gspread.authorize(credentials)
            print("Google Sheets client authenticated successfully.")
            return client
        except Exception as e:
            print(f"Error authenticating with Google Sheets: {e}")
            return None
        
    def init_sheet(self):
        try:
            spreadsheet = self.client.open_by_key(self.sheet_id)
            try:
                self.worksheet = spreadsheet.worksheet(self.sheet_name)
                print(f"Worksheet '{self.sheet_name}' already exists.")
            except gspread.WorksheetNotFound:
                self.worksheet = spreadsheet.add_worksheet(title=self.sheet_name, rows="100", cols="20")
                self.worksheet.append_row(SHEET_HEADERS)
                print(f"Worksheet '{self.sheet_name}' created successfully.")
            return self.worksheet
        except Exception as e:
            print(f"Error initializing Google Sheet: {e}")
            return None
    
    def get_sheet_headers(self):
        if self.worksheet:
            return self.worksheet.row_values(1)
    def verify_sheet(self):
        if self.get_sheet_headers() != SHEET_HEADERS:
            print("Sheet headers do not match. Try changing the sheet name or check the headers.")
            return False
        print("Sheet headers verified successfully.")
        return True
    
    def get_channel_url(self, row_line):
        if self.worksheet:
            try:
                return self.worksheet.cell(row_line, 2).value
            except gspread.exceptions.CellNotFound:
                print(f"Cell at row {row_line} not found.")
                return None
    def get_channel_name(self, row_line):
        if self.worksheet:
            try:
                return self.worksheet.cell(row_line, 1).value
            except gspread.exceptions.CellNotFound:
                print(f"Cell at row {row_line} not found.")
                return None

            
        