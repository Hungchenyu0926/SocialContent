import gspread
from datetime import datetime
import streamlit as st

def save_to_sheet(topic, keywords, url, content):
    try:
        # 驗證並建立連線
        gc = gspread.service_account_from_dict(st.secrets["GSPREAD_CREDENTIALS"])
        
        # 開啟試算表（注意此處名稱需和您的 Google Sheets 標題完全相符）
        sh = gc.open("SmartMeds_DB")  # 可改成您實際建立的文件名稱
        worksheet = sh.worksheet("social_content")  # 頁籤名稱也需一致

        # 組合資料列
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 時間戳記
            topic,
            keywords,
            url,
            content
        ]

        # 寫入下一列
        worksheet.append_row(row, value_input_option="USER_ENTERED")
    
    except Exception as e:
        st.error(f"❌ 無法寫入 Google Sheet：{str(e)}")
