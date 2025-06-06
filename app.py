import streamlit as st
import openai
import pandas as pd
import requests
from bs4 import BeautifulSoup
from utils.gsheet import save_to_sheet  # 確保您有正確實作此模組

# 設定 OpenAI API 金鑰
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 設定 Streamlit 頁面資訊
st.set_page_config(page_title="社群圖文生成器", layout="wide")
st.title("🤖 AI社群圖文自動生成 App")
st.markdown("請於 Google Sheet 中填入主題、關鍵字與網址")

# 讀取 Google Sheet 資料
sheet_id = st.secrets["SHEET_ID"]
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
df = pd.read_csv(csv_url)

st.subheader("📝 原始資料")
st.dataframe(df)

# 網頁內容擷取函式
def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join([p.text for p in paragraphs[:5]])
    except Exception as e:
        return f"⚠️ 無法擷取網址內容: {str(e)}"

st.subheader("📤 AI 生成內容")

# 逐列處理每個主題
for index, row in df.iterrows():
    with st.expander(f"主題：{row['主題']}"):
        keywords = row['關鍵字']
        url = row['網址']
        external_content = fetch_url_content(url)

        full_prompt = f"""
你是一位社群行銷內容撰寫助手。請根據以下資訊生成一篇適合貼在 Facebook 的貼文，並建議一張圖片的圖像風格與畫面主題：

主題：{row['主題']}
關鍵字：{keywords}
網址內容摘要：{external_content}

請輸出格式如下：
1. 貼文文字（繁體中文）
2. 推薦圖片描述（圖像風格 + 畫面元素）
"""

        if st.button(f"產生：{row['主題']}", key=f"btn_{index}"):
            with st.spinner("AI 正在生成中..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                generated = response.choices[0].message.content.strip()
                st.markdown("#### ✨ 生成內容")
                st.markdown(generated)
