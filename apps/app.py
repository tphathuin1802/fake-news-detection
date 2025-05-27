import pickle
import re

import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(page_title="🕵️‍♂️ Fake News Detector", layout="centered")

st.markdown(
    """
    <style>
    * {
        font-family: 'Roboto Mono', monospace !important;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_components():
    with open("../models/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("../models/lr.pkl", "rb") as f:
        lr = pickle.load(f)
    with open("../models/gbc.pkl", "rb") as f:
        gbc = pickle.load(f)
    with open("../models/rfc.pkl", "rb") as f:
        rfc = pickle.load(f)
    return vectorizer, lr, gbc, rfc


def wordopt(text):
    text = text.lower()
    text = re.sub(r"https?://\S+www\.\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\d", " ", text)
    text = re.sub(r"\n", " ", text)
    return text


def output_label(n):
    return "🧨 Fake News" if n == 0 else "✅ True News"


def manualPredict(news, vectorizer, lr, gbc, rfc):
    news_def_test = pd.DataFrame({"text": [news]})
    news_def_test["text"] = news_def_test["text"].apply(wordopt)
    news_xv_test = vectorizer.transform(news_def_test["text"])

    pred_lr = lr.predict(news_xv_test)[0]
    pred_gbc = gbc.predict(news_xv_test)[0]
    pred_rfc = rfc.predict(news_xv_test)[0]

    preds = [pred_lr, pred_gbc, pred_rfc]
    fake_count = preds.count(0)

    result_text = f"""
    🤖 **LR Prediction:** {output_label(pred_lr)}  
    🌐 **GBC Prediction:** {output_label(pred_gbc)}  
    🌲 **RFC Prediction:** {output_label(pred_rfc)}  
    """

    conclusion = (
        "💥 **Conclusion:** This is likely *FAKE NEWS*! ❌"
        if fake_count >= 2
        else "✅ **Conclusion:** This is likely *TRUE NEWS*! 🎉"
    )
    return result_text + "\n\n" + conclusion


st.title("🕵️‍♂️ Fake News Detection App")

image = Image.open("../assets/image.png")
st.image(image, width=400)

vectorizer, lr, gbc, rfc = load_components()

user_input = st.text_area("📰 Input the article news you want to check:")

if st.button("🔍 Predict"):
    if user_input.strip() == "":
        st.warning("⚠️ Please input the article carefully.")
    else:
        prediction = manualPredict(user_input, vectorizer, lr, gbc, rfc)
        st.markdown(prediction)
