import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import streamlit as st
import datetime

def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("SocialContent_DB").sheet1

def save_to_sheet(topic, keywords, post_text, image_url, url):
    sheet = connect_to_gsheet()
    sheet.append_row([datetime.datetime.now().isoformat(), topic, keywords, post_text, image_url, url])
