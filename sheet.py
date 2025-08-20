import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube import YouTubeAPI
from pprint import pprint

class GoogleSheetsAPI:

    SHEET_HEADERS = ["Name", "URL"]

    def __init__(self, sheet_name="sheet"):
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.sheet_name = sheet_name

        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        
        ]
        self.client = self.authenticate()
        self.spreadsheet = self.client.open_by_key(self.sheet_id)
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
        
    def build_service(self):
        try:
            credentials = Credentials.from_service_account_file(self.credentials_file,
                                                                scopes = self.scope)
            client = gspread.authorize(credentials)
            return client
        except Exception as e:
            print(f"Error building service {e}")

    def init_sheet(self):
        try:
            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            print(f"Worksheet '{self.sheet_name}' already exists.")
        except:
            worksheet = self.spreadsheet.add_worksheet(
                title=self.sheet_name, rows="100", cols="20"
            )
            print(f"Worksheet '{self.sheet_name}' created successfully.")
        existing_headers = worksheet.row_values(1) 
        if not existing_headers:  
            worksheet.append_row(self.SHEET_HEADERS)
            print(f"Headers inserted: {self.SHEET_HEADERS}")
        else:
            print(f"Headers already present: {existing_headers}")
        return worksheet

    
    def get_sheet_headers(self):
        if self.worksheet:
            return self.worksheet.row_values(1)
    def verify_sheet(self):
        if self.get_sheet_headers() != self.SHEET_HEADERS:
            print("Sheet headers do not match. Try changing the sheet name or check the headers.")
            return False
        print("Sheet headers verified successfully.")
        return True
    
    def get_channel_url(self, row_line):
        worksheet = self.spreadsheet.worksheet(self.sheet_name)
        try:
            return worksheet.cell(row_line, 2).value
        except gspread.exceptions.CellNotFound:
            print(f"Cell at row {row_line} not found.")
            return None
    def get_channel_name(self, row_line):
        worksheet = self.spreadsheet.worksheet(self.sheet_name)
        try:
            return worksheet.cell(row_line, 1).value
        except gspread.exceptions.CellNotFound:
            print(f"Cell at row {row_line} not found.")
            return None
        
    def get_channel_info(self, row, videos=10):
        try:
            return YouTubeAPI().get_channel_info(self.get_channel_url(row), videos=videos)
        except Exception as e:
            print(f"Error getting channel info from row={row}: {e}")
            return None
    
    def get_num_sheet_rows(self, sheet_name):
        try:
            worksheet_metadata = self.spreadsheet.fetch_sheet_metadata()

            for sheet in worksheet_metadata["sheets"]:
                if sheet["properties"]["title"] == sheet_name:
                    row_count = sheet["properties"]["gridProperties"]["rowCount"]
                    return row_count
        except:
            print(f"Sheet {sheet_name} not fount")
            return None
    def create_new_sheet(self, sheet_name):
        if sheet_name == None:
            return None
        try:
            print(f"sheet_name ={sheet_name}")
            self.worksheet = self.spreadsheet.worksheet(sheet_name)
            print("Worksheet already exists")
        except:
            self.worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=100)
            print(f"Worksheet {sheet_name} created successfully")

    def append_rows(self, data, validate_keys=True):
        try:
            if not self.worksheet:
                print("Worksheet not initialized")

            # getting all values of the table
            print("getting all_data")
            all_data = self.worksheet.get_all_values()
            print(f"all_data={all_data}")

            if not all_data[0]:   # table is empty -> create headers from dictionary keys
                print("appending to clear table")
                headers = data[0].keys()
                pprint(headers)
                self.worksheet.append_row(list(headers))
                for i in data:
                    self.worksheet.append_row([str(k) for k in i.values()])
            
            elif validate_keys:
                print("validating keys...")
                headers_external = data[0].keys()
                headers_internal = self.worksheet.row_values(0)
                if headers_external != headers_internal:
                    print("Can't add new data to table: headers misalignment!")
                    print(f"internal: {headers_internal}")
                    print(f"external: {headers_external}")
                for i in data:
                    self.worksheet.append_row([str(k) for k in i.values()])
            
            else:
                print("else condition")
                for i in data:
                    self.worksheet.append_row(str(k) for k in i.values())

        except Exception as e:
            print(f"Error while appending row {e}")


            