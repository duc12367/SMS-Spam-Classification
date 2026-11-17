"""Ứng dụng demo (Streamlit):  streamlit run app.py"""
import sys
from pathlib import Path

import joblib
import numpy as np
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from predict import load_model  # noqa: E402

st.set_page_config(page_title="SMS Spam Classifier", page_icon="📩")
st.title("📩 Phân loại tin nhắn rác (SMS Spam)")
st.caption("Mô hình huấn luyện trên SMS Spam Collection (UCI). Tin nhắn tiếng Anh.")

name_map = {"Tốt nhất theo CV": None, "Multinomial NB": "nb", "K-NN": "knn", "Decision Tree": "dt"}
choice = st.sidebar.selectbox("Mô hình", list(name_map))
threshold = st.sidebar.slider("Ngưỡng P(spam)", 0.05, 0.95, 0.5, 0.05)
name, model = load_model(name_map[choice])

text = st.text_area("Nhập nội dung tin nhắn", "WINNER!! You have won a £1000 prize. Call 09061701461 to claim.", height=120)
if st.button("Phân loại") and text.strip():
    p = float(model.predict_proba([text])[0, 1])
    (st.error if p >= threshold else st.success)(f"{'SPAM' if p >= threshold else 'HAM'}  –  P(spam) = {p:.3f}  ({name})")
    if name == "nb":
        vec, clf = model.named_steps["vec"], model.named_steps["clf"]
        names = np.array(vec.get_feature_names_out())
        x = vec.transform([text])
        contrib = x.multiply(clf.feature_log_prob_[1] - clf.feature_log_prob_[0]).tocoo()
        if contrib.nnz:
            order = np.argsort(-np.abs(contrib.data))[:8]
            st.subheader("Từ ảnh hưởng nhiều nhất (log-odds spam/ham)")
            st.table({"Từ": names[contrib.col[order]], "Đóng góp": np.round(contrib.data[order], 2)})
