import streamlit as st
from openai import OpenAI
import pandas as pd
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from utils.gsheet import save_to_sheet

# 初始化 OpenAI client（使用 secrets）
openai_api_key = st.secrets["OPENAI"]["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)


st.set_page_config(page_title="社群圖文生成器", layout="wide")

st.title("🤖 AI社群圖文自動生成 App")
st.markdown("請於 Google Sheet 中填入主題、關鍵字與網址")

# 從 Google Sheet 讀取資料
sheet_id = st.secrets["SHEET_ID"]
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
df = pd.read_csv(sheet_url)

st.subheader("📝 原始資料")
st.dataframe(df)

def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join([p.text for p in paragraphs[:5]])  # 簡略擷取前五段
    except Exception as e:
        return f"無法擷取網址內容: {str(e)}"

st.subheader("📤 AI 生成內容")

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
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": full_prompt}]
                )

                generated = response.choices[0].message.content.strip()
                st.markdown("#### ✨ 生成內容")
                st.markdown(generated)

                # 儲存到 Google Sheet
                save_to_sheet(row['主題'], keywords, url, generated)
                st.success("已儲存至 Google Sheet ✅")
