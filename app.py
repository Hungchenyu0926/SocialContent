import streamlit as st
import pandas as pd
from openai import OpenAI
import urllib.request

# 初始化 OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 頁面設定
st.set_page_config(page_title="社群貼文產生器", layout="wide")
st.title("🤖 AI 社群貼文產生器")

# 載入資料
csv_url = "https://raw.githubusercontent.com/Hungchenyu0926/socialcontent/main/social_posts.csv"

try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"無法載入資料，請檢查連結或格式錯誤。\n錯誤訊息: {e}")
    st.stop()

# UI: 選擇貼文主題與目標對象
col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox("🎯 選擇貼文主題", df["title"].dropna().unique())

with col2:
    target = st.selectbox("👥 選擇目標對象", df["text"].dropna().unique())

# 過濾資料
filtered_df = df[(df["title"] == topic) & (df["text"] == target)]

if not filtered_df.empty:
    row = filtered_df.iloc[0]
    keyword = row["keyword"]
    purpose = row["purpose"]

    # 建立 Prompt
    full_prompt = f"""
你是一位社群行銷專家，請根據以下條件設計一則社群貼文建議與一張圖片描述：

主題：{topic}
目標對象：{target}
關鍵詞：{keyword}
目的：{purpose}

請產出：
1. 一段吸引人的貼文內容（不超過 100 字）
2. 一句圖片描述，用於生成 AI 圖像（不超過 50 字）
"""

    # 呼叫 OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )
        result = response.choices[0].message.content
        st.subheader("✅ 產生內容如下：")
        st.markdown(result)
    except Exception as e:
        st.error(f"產生內容時發生錯誤：\n{e}")
else:
    st.warning("找不到符合條件的資料，請確認 CSV 檔案內容是否正確。")



