import streamlit as st
import pandas as pd
import openai
import requests
from io import StringIO

# 🚀 設定 OpenAI API Key（建議從 secrets 管理）
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🧾 讀取 CSV 資料
csv_url = "https://raw.githubusercontent.com/Hungchenyu0926/socialcontent/main/social_posts.csv"

try:
    response = requests.get(csv_url)
    response.raise_for_status()
    df = pd.read_csv(StringIO(response.text))
    df.columns = df.columns.str.strip()  # 移除欄位名稱空白
except Exception as e:
    st.error(f"無法載入資料，請檢查連結或格式錯誤。\n錯誤訊息: {e}")
    st.stop()

st.title("🎯 社群貼文產生器 SmartPost-AI")

# 使用者選單
col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox("📌 選擇貼文主題", df["title"].dropna().unique())

with col2:
    target = st.selectbox("👥 選擇目標對象", df["text"].dropna().unique())

# 過濾符合條件的資料
filtered_df = df[(df["title"] == topic) & (df["text"] == target)]

if not filtered_df.empty:
    row = filtered_df.iloc[0]
    keyword = row["keyword"]
    purpose = row["purpose"]

    # 建立 Prompt
    full_prompt = f"""
你是一位社群行銷專家，請根據以下條件設計一則社群貼文建議與一張圖片描述：

🎯 主題: {topic}
👥 目標對象: {target}
🔑 關鍵詞: {keyword}
🎯 目的: {purpose}

請輸出：
1. 一段吸引人的社群貼文內容（約100字）
2. 一段圖片敘述（提示給 AI 畫圖用，約30字）
"""

    # 呼叫 OpenAI GPT-4 API 產生內容
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}]
        )
        result = response["choices"][0]["message"]["content"]
        st.success("🎉 貼文與圖片提示產生完成！")
        st.markdown(result)

    except Exception as e:
        st.error(f"產生內容時發生錯誤：{e}")

else:
    st.warning("❗ 沒有符合的資料，請重新選擇主題與對象。")


