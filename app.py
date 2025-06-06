import streamlit as st
import pandas as pd
from openai import OpenAI

# 初始化 OpenAI 客戶端（使用 Streamlit Secrets 儲存 API 金鑰）
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 頁面標題與說明
st.set_page_config(page_title="社群內容產生器", layout="centered")
st.title("📱 AI 社群內容生成器")
st.markdown("請從下拉選單中選擇主題與對象，我們將自動生成貼文建議與圖片描述。")

# 載入資料（CSV 來自 GitHub Sheets 的 raw 連結）
csv_url = "https://raw.githubusercontent.com/Hungchenyu0926/SocialContent/main/social_posts.csv"


@st.cache_data
def load_data():
    return pd.read_csv(csv_url)

try:
    df = load_data()
except Exception as e:
    st.error(f"無法載入資料，請檢查連結或格式錯誤。\n錯誤訊息: {e}")
    st.stop()

# 使用者選擇欄位
col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox("🎯 選擇貼文主題", df["主題"].dropna().unique())

with col2:
    target = st.selectbox("👥 選擇目標對象", df["對象"].dropna().unique())

# 過濾資料
filtered_df = df[(df["主題"] == topic) & (df["對象"] == target)]

if not filtered_df.empty:
    row = filtered_df.iloc[0]
    keyword = row["關鍵詞"]
    purpose = row["目的"]

    # 建立 Prompt
    full_prompt = f"""
你是一位社群行銷專家，請根據以下條件設計一則社群貼文建議與一張圖片描述。

主題: {topic}
對象: {target}
關鍵詞: {keyword}
目的: {purpose}

請輸出格式如下：
---
貼文建議：
（請以繁體中文撰寫一則適合的社群貼文內容）

圖片描述建議：
（建議的圖片視覺元素與風格）
"""

    if st.button("🎨 產生社群內容"):
        with st.spinner("生成中，請稍候..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                result_text = response.choices[0].message.content
                st.success("產生完成 ✅")
                st.markdown(result_text)

            except Exception as e:
                st.error(f"OpenAI 回傳錯誤: {e}")

else:
    st.warning("查無符合的主題與對象組合，請重新選擇。")

